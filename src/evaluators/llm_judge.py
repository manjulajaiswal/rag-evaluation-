import json
import os

from google import genai


class LLMJudge:
    def __init__(self):
        self.client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY")
        )

    def evaluate(
        self,
        question,
        expected_answer,
        generated_answer,
        context
    ):
        prompt = f"""
You are an evaluator for a Retrieval-Augmented Generation (RAG) system.

Evaluate the generated answer using:
- the user's question,
- the expected answer,
- and the retrieved context.

Your evaluation must distinguish between two independent properties:

1. FAITHFULNESS
2. CORRECTNESS

Do not assume that a correct answer is necessarily faithful, or that a
faithful answer is necessarily correct.

==================================================
QUESTION
==================================================

{question}

==================================================
EXPECTED ANSWER
==================================================

{expected_answer}

==================================================
GENERATED ANSWER
==================================================

{generated_answer}

==================================================
RETRIEVED CONTEXT
==================================================

{context}

==================================================
FAITHFULNESS EVALUATION
==================================================

Evaluate whether the generated answer is supported by the retrieved context.

First, decompose the generated answer into its smallest meaningful factual
claims.

For each claim, determine whether the claim can be directly supported or
reasonably inferred from the retrieved context.

A claim is faithful if:
- it is explicitly stated in the context, OR
- it is a reasonable conclusion obtained by combining information from the
  provided context.

A claim is NOT faithful if:
- it introduces information absent from the context,
- it relies on outside knowledge,
- it adds an unsupported detail,
- it contradicts the context,
- or it makes a stronger claim than the context supports.

Do NOT penalize harmless wording differences or reasonable paraphrasing.

Faithfulness score:

- 1 = every meaningful factual claim is supported by the retrieved context.
- 0 = at least one meaningful factual claim is unsupported or contradicted.

==================================================
CORRECTNESS EVALUATION
==================================================

Evaluate whether the generated answer correctly answers the question.

Compare the generated answer against the expected answer.

Consider:

- factual agreement,
- whether the main required information is present,
- whether important information is missing,
- whether the answer directly addresses the question,
- whether the generated answer contradicts the expected answer.

Do NOT require identical wording.

A generated answer can be correct even if it is shorter or phrased differently
from the expected answer.

However, mark correctness as 0 if the answer contains a material factual error,
contradiction, or fails to answer an important part of the question.

==================================================
IMPORTANT DISTINCTION
==================================================

Use the retrieved context ONLY for judging faithfulness.

Use the expected answer as the reference for judging correctness.

For example:

- Correct + faithful:
  The answer is supported by the context and agrees with the expected answer.

- Correct + unfaithful:
  The answer agrees with the expected answer but contains additional
  unsupported claims.

- Incorrect + faithful:
  The answer only uses information found in the context but fails to answer
  the question correctly.

- Incorrect + unfaithful:
  The answer contains unsupported or incorrect claims and does not match the
  expected answer.

==================================================
OUTPUT
==================================================

Return ONLY valid JSON.

Use exactly this schema:

{{
    "correctness": 0,
    "faithfulness": 0
}}

Use only integer values 0 or 1.
Do not include markdown.
Do not include explanations outside the JSON.
"""

        response = self.client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )

        text = response.text.strip()

        if text.startswith("```"):
            text = text.replace("```json", "")
            text = text.replace("```", "")
            text = text.strip()

        return json.loads(text)