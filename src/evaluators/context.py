import json
import os
import time

from google import genai


class ContextJudge:
    def __init__(
        self,
        model="gemini-3.5-flash-lite",
        request_delay=4
    ):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY environment variable is not set."
            )

        self.client = genai.Client(api_key=api_key)
        self.model = model
        self.request_delay = request_delay

    def _parse_json(self, text):
        """Parse normal JSON or JSON wrapped in markdown fences."""

        text = text.strip()

        if text.startswith("```"):
            lines = text.splitlines()

            if lines and lines[0].strip().startswith("```"):
                lines = lines[1:]

            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]

            text = "\n".join(lines).strip()

        return json.loads(text)

    def _call_llm(self, prompt):
        """Call Gemini and parse the JSON response."""

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )

        if not response.text:
            raise ValueError(
                "LLM returned an empty response."
            )

        return self._parse_json(response.text)

    def evaluate_context(
        self,
        question,
        reference_answer,
        retrieved_chunks
    ):
        """
        Evaluate both Context Precision and Context Recall
        in a single LLM call.

        Context Precision:
        Judge whether each retrieved chunk supports information
        needed to answer the question.

        Context Recall:
        Decompose the reference answer into atomic claims and
        determine whether the retrieved context supports each claim.
        """

        chunks_text = []

        for rank, chunk in enumerate(
            retrieved_chunks,
            start=1
        ):
            chunks_text.append(
                f"""
CHUNK {rank}
Chunk ID: {chunk["chunk_id"]}
Document ID: {chunk["document_id"]}

{chunk["text"]}
"""
            )

        context = "\n".join(chunks_text)

        prompt = f"""
You are evaluating retrieval quality in a
Retrieval-Augmented Generation (RAG) system.

You must evaluate BOTH:

1. CONTEXT PRECISION
2. CONTEXT RECALL

Do NOT use outside knowledge.

==================================================
QUESTION
==================================================

{question}

==================================================
REFERENCE ANSWER
==================================================

{reference_answer}

==================================================
RETRIEVED CHUNKS
==================================================

{context}

==================================================
CONTEXT PRECISION
==================================================

For each retrieved chunk, determine whether it contains information
that supports at least one specific factual claim needed to produce
the reference answer.

A chunk is RELEVANT only when it provides useful answer-supporting
information.

Do NOT mark a chunk relevant merely because:
- it discusses the same topic,
- it mentions the same model or entity,
- it is generally related to the question.

For each chunk:

1 = relevant and useful for answering the question
0 = not relevant/useful for the answer

A useful chunk may support one or more parts of the reference answer.

==================================================
CONTEXT RECALL
==================================================

Decompose the reference answer into its smallest meaningful factual
claims.

For each claim, determine whether the retrieved chunks support it.

A claim is SUPPORTED if:
- it is explicitly stated in the retrieved chunks, OR
- it can reasonably be inferred by combining retrieved chunks.

A claim is NOT SUPPORTED if:
- it is absent,
- the retrieved chunks contradict it,
- or outside knowledge would be required.

For every claim, provide a short reason based ONLY on the retrieved chunks.

==================================================
OUTPUT
==================================================

Return ONLY valid JSON.

Use exactly this schema:

{{
    "chunk_judgments": [
        {{
            "rank": 1,
            "relevant": 1,
            "reason": "short explanation"
        }}
    ],
    "claims": [
        {{
            "claim": "claim text",
            "supported": 1,
            "reason": "short explanation"
        }}
    ]
}}

Use only:
1 = relevant/supported
0 = not relevant/not supported
"""

        result = self._call_llm(prompt)

        if "chunk_judgments" not in result:
            raise ValueError(
                "Context evaluation response is missing "
                "'chunk_judgments'."
            )

        if "claims" not in result:
            raise ValueError(
                "Context evaluation response is missing "
                "'claims'."
            )

        chunk_judgments = result["chunk_judgments"]
        claims = result["claims"]

        if not isinstance(chunk_judgments, list):
            raise ValueError(
                "'chunk_judgments' must be a list."
            )

        if not isinstance(claims, list):
            raise ValueError(
                "'claims' must be a list."
            )

        validated_chunks = []

        for judgment in chunk_judgments:

            if (
                not isinstance(judgment, dict)
                or "rank" not in judgment
                or "relevant" not in judgment
                or "reason" not in judgment
            ):
                raise ValueError(
                    "Invalid chunk judgment structure."
                )

            relevant = int(judgment["relevant"])

            if relevant not in (0, 1):
                raise ValueError(
                    f"Invalid chunk relevance value: {relevant}"
                )

            validated_chunks.append({
                "rank": int(judgment["rank"]),
                "relevant": relevant,
                "reason": str(
                    judgment["reason"]
                ).strip()
            })

        validated_claims = []

        for claim in claims:

            if (
                not isinstance(claim, dict)
                or "claim" not in claim
                or "supported" not in claim
                or "reason" not in claim
            ):
                raise ValueError(
                    "Invalid claim structure."
                )

            supported = int(claim["supported"])

            if supported not in (0, 1):
                raise ValueError(
                    f"Invalid claim support value: {supported}"
                )

            validated_claims.append({
                "claim": str(
                    claim["claim"]
                ).strip(),

                "supported": supported,

                "reason": str(
                    claim["reason"]
                ).strip()
            })

        context_recall = (
            sum(
                claim["supported"]
                for claim in validated_claims
            ) / len(validated_claims)
            if validated_claims
            else 0
        )

        return {
            "chunk_judgments": validated_chunks,
            "claims": validated_claims,
            "context_recall": context_recall
        }

    def evaluate_chunk_relevance(
        self,
        question,
        reference_answer,
        retrieved_chunks
    ):
        """
        Backward-compatible wrapper.

        Uses the batched context evaluator and returns only the
        chunk relevance judgments.
        """

        result = self.evaluate_context(
            question=question,
            reference_answer=reference_answer,
            retrieved_chunks=retrieved_chunks
        )

        output = []

        for judgment in result["chunk_judgments"]:

            rank = judgment["rank"]

            chunk = retrieved_chunks[rank - 1]

            output.append({
                "rank": rank,
                "chunk_id": chunk["chunk_id"],
                "document_id": chunk["document_id"],
                "relevant": judgment["relevant"],
                "reason": judgment["reason"]
            })

        time.sleep(self.request_delay)

        return output

    def evaluate_context_recall(
        self,
        question,
        reference_answer,
        retrieved_chunks
    ):
        """
        Backward-compatible wrapper.

        Uses the same batched context evaluation and returns only
        the Context Recall portion.
        """

        result = self.evaluate_context(
            question=question,
            reference_answer=reference_answer,
            retrieved_chunks=retrieved_chunks
        )

        time.sleep(self.request_delay)

        return {
            "score": result["context_recall"],
            "claims": result["claims"]
        }


def calculate_context_precision(chunk_results):
    """
    Calculate rank-aware Context Precision.

    Relevant chunks appearing earlier in the ranking receive more weight.
    """

    if not chunk_results:
        return 0

    relevant_count = 0
    precision_sum = 0

    for rank, chunk in enumerate(
        chunk_results,
        start=1
    ):

        if chunk["relevant"] == 1:

            relevant_count += 1

            precision_at_rank = (
                relevant_count / rank
            )

            precision_sum += (
                precision_at_rank
            )

    if relevant_count == 0:
        return 0

    return (
        precision_sum / relevant_count
    )