import json
import glob
import os


METRICS = [
    "document_precision",
    "document_recall",
    "context_precision",
    "context_recall",
    "faithfulness",
    "correctness",
    "ragas_style_composite"
]


def load_results(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def print_experiment(title, results_a, results_b):
    scores_a = results_a["aggregate_scores"]
    scores_b = results_b["aggregate_scores"]

    config_a = results_a["configuration"]["config_name"]
    config_b = results_b["configuration"]["config_name"]

    print("\n" + "=" * 95)
    print(title)
    print("=" * 95)

    print(
        f"{'Metric':<28}"
        f"{config_a:<18}"
        f"{config_b:<18}"
        f"{'Winner':<25}"
    )
    print("-" * 95)

    for metric in METRICS:
        score_a = scores_a.get(metric, 0)
        score_b = scores_b.get(metric, 0)

        if score_a > score_b:
            winner = config_a
        elif score_b > score_a:
            winner = config_b
        else:
            winner = "Tie"

        print(
            f"{metric:<28}"
            f"{score_a:<18.3f}"
            f"{score_b:<18.3f}"
            f"{winner:<25}"
        )


def create_summary(results):
    summary = []

    for result in results:
        config = result["configuration"]

        row = {
            "experiment": config["experiment"],
            "configuration": config["config_name"],
            "chunk_size": config["chunk_size"],
            "overlap": config["overlap"],
            "top_k": config["top_k"],
            "embedding_model": config["embedding_model"]
        }

        row.update(result["aggregate_scores"])
        summary.append(row)

    return summary


def print_all_results(results):
    print("\n" + "=" * 110)
    print("FINAL RAG EVALUATION MATRIX")
    print("=" * 110)

    headers = [
        "Configuration",
        "Doc P",
        "Doc R",
        "Ctx P",
        "Ctx R",
        "Faith.",
        "Correct.",
        "Composite"
    ]

    print(
        f"{headers[0]:<20}"
        f"{headers[1]:<9}"
        f"{headers[2]:<9}"
        f"{headers[3]:<9}"
        f"{headers[4]:<9}"
        f"{headers[5]:<9}"
        f"{headers[6]:<9}"
        f"{headers[7]:<10}"
    )

    print("-" * 110)

    for result in results:
        scores = result["aggregate_scores"]
        name = result["configuration"]["config_name"]

        print(
            f"{name:<20}"
            f"{scores['document_precision']:<9.3f}"
            f"{scores['document_recall']:<9.3f}"
            f"{scores['context_precision']:<9.3f}"
            f"{scores['context_recall']:<9.3f}"
            f"{scores['faithfulness']:<9.3f}"
            f"{scores['correctness']:<9.3f}"
            f"{scores['ragas_style_composite']:<10.3f}"
        )


def print_best_configuration(results):
    best = max(
        results,
        key=lambda r: r["aggregate_scores"]["ragas_style_composite"]
    )

    config = best["configuration"]
    scores = best["aggregate_scores"]

    print("\n" + "=" * 95)
    print("BEST CONFIGURATION")
    print("=" * 95)

    print(f"Configuration: {config['config_name']}")
    print(f"Chunk size: {config['chunk_size']}")
    print(f"Overlap: {config['overlap']}")
    print(f"Top-k: {config['top_k']}")
    print(f"Embedding: {config['embedding_model']}")

    print("\nScores:")
    for metric in METRICS:
        print(
            f"{metric:<28}: "
            f"{scores.get(metric, 0):.3f}"
        )


if __name__ == "__main__":

    result_files = sorted(
        glob.glob("results/*_results.json")
    )

    result_files = sorted(
    glob.glob("results/*_results.json")
)

loaded_results = []

for path in result_files:
    try:
        result = load_results(path)

        if not isinstance(result, dict):
            print(f"Skipping {path}: expected a JSON object.")
            continue

        if "aggregate_scores" not in result:
            print(f"Skipping {path}: missing aggregate_scores.")
            continue

        loaded_results.append(result)

    except Exception as error:
        print(f"Skipping {path}: {error}")

    if not loaded_results:
        print("No result files found.")
        raise SystemExit(1)

    print_all_results(loaded_results)

    print("\n" + "=" * 95)
    print("CONTROLLED EXPERIMENT COMPARISONS")
    print("=" * 95)

    by_name = {
        result["configuration"]["config_name"]: result
        for result in loaded_results
    }

    if "chunk_small" in by_name and "chunk_large" in by_name:
        print_experiment(
            "Experiment 1: Chunk Size",
            by_name["chunk_small"],
            by_name["chunk_large"]
        )

    if "topk_2" in by_name and "topk_5" in by_name:
        print_experiment(
            "Experiment 2: Top-k",
            by_name["topk_2"],
            by_name["topk_5"]
        )

    if "embed_minilm" in by_name and "embed_mpnet" in by_name:
        print_experiment(
            "Experiment 3: Embedding Model",
            by_name["embed_minilm"],
            by_name["embed_mpnet"]
        )

    print_best_configuration(loaded_results)

    summary = create_summary(loaded_results)

    summary_path = "results/comparison_summary.json"

    with open(
        summary_path,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            summary,
            file,
            indent=2,
            ensure_ascii=False
        )

    print("\n" + "=" * 95)
    print(f"Saved: {summary_path}")
    print("=" * 95)