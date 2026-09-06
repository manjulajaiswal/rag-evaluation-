from generator import Generator


generator = Generator()

question = "When was NovaTech founded?"

context = """
NovaTech is a technology company founded in 2018 by Maya Chen and Daniel Brooks.
The company is headquartered in Austin, Texas.
"""

answer = generator.generate(
    question,
    context
)

print("Question:", question)
print("\nAnswer:", answer)