import json

with open("data/eval_questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

print("Number of questions:", len(questions))

for q in questions:
    print(q["id"], "->", q["question"])

print("\nDataset loaded successfully.")