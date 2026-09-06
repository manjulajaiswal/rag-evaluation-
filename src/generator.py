import os
from google import genai


class Generator:
    def __init__(self):
        self.client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY")
        )

    def generate(self, question, context):
        prompt = f"""
Answer the question using only the provided context.

If the answer cannot be found in the context, say:
"I don't have enough information in the provided context."

Context:
{context}

Question:
{question}

Answer:
"""

        response = self.client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )

        return response.text