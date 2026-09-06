from evaluators.llm_judge import LLMJudge


judge = LLMJudge()

question = "When was NovaTech founded and who founded it?"

expected_answer = (
    "NovaTech was founded in 2018 by Maya Chen and Daniel Brooks."
)

generated_answer = (
    "NovaTech was founded in 2018 by Maya Chen and Daniel Brooks. "
    "Its headquarters are in London."
)

context = """
NovaTech is a technology company founded in 2018 by Maya Chen and Daniel Brooks.
The company is headquartered in Austin, Texas.
"""

result = judge.evaluate(
    question,
    expected_answer,
    generated_answer,
    context
)

print("Judge result:")
print(result)