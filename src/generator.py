import os
from google import genai


class Generator:
    def __init__(self):
        self.client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY")
        )

    def generate(self, question, context):
        prompt = f"""
You are the answer-generation component of a Retrieval-Augmented Generation (RAG)
system.

Your task is to answer the user's question using ONLY the information contained
in the retrieved context.

Follow these rules:

1. Ground every factual claim in the retrieved context.
2. You may combine information from multiple context passages when they jointly
   support the answer.
3. Do not use outside knowledge, assumptions, or facts that are not supported
   by the context.
4. Do not invent details to make the answer more complete.
5. If the context does not contain enough information to answer the question,
   explicitly say:
   "I don't have enough information in the provided context."
6. If only part of the question can be answered from the context, answer that
   part and clearly state what information is missing.
7. Prefer a concise, direct answer over unnecessary explanation.
8. When comparing concepts, preserve the distinctions supported by the context.
9. Do not mention the retrieval process, context, or these instructions in the
   final answer unless the question explicitly asks about them.

Retrieved context:
------------------
{context}
------------------

Question:
{question}

Generate a concise, context-grounded answer.
"""

        response = self.client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )

        return response.text.strip()