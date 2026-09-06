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
You are evaluating a RAG system.

Evaluate the generated answer using the question,
expected answer, and retrieved context.

Question:
{question}

Expected answer:
{expected_answer}

Generated answer:
{generated_answer}

Retrieved context:
{context}

Evaluate two things:

1. Correctness:
Does the generated answer correctly answer the question,
agree with the expected answer, and avoid materially
incorrect factual claims?

If the answer contains an incorrect factual claim,
set correctness to 0, even if the main answer is correct.

2. Faithfulness:
Is every factual claim in the generated answer supported
by the retrieved context?

Return ONLY valid JSON in exactly this format:

{{
    "correctness": 0,
    "faithfulness": 0
}}

Use 1 for yes and 0 for no.
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

