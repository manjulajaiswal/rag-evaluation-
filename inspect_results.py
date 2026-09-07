import json

with open("results/chunk_small_results.json", "r", encoding="utf-8") as file:
    data = json.load(file)

for r in data["results"]:
    print(
        f"{r['id']} | "
        f"{r['type']} | "
        f"P={r['retrieval_precision']:.2f} "
        f"R={r['retrieval_recall']:.2f} "
        f"F={r['faithfulness']:.2f} "
        f"C={r['correctness']:.2f} | "
        f"retrieved={r['retrieved_documents']}"
    )