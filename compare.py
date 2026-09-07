import json
import os


RESULT_FILES = [
    "results/chunk_small_results.json",
    "results/chunk_large_results.json",
    "results/topk_2_results.json",
    "results/topk_5_results.json",
    "results/embed_minilm_results.json",
    "results/embed_mpnet_results.json",
    "results/final_combined_results.json"
]


def load_results(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def print_experiment(title, results_a, results_b):
    scores_a = results_a["aggregate_scores"]
    scores_b = results_b["aggregate_scores"]

    config_a = results_a["configuration"]["config_name"]
    config_b = results_b["configuration"]["config_name"]

    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)

    print(
        f"{'Metric':<25}"
        f"{config_a:<15}"
        f"{config_b:<15}"
        f"{'Winner':<15}"
    )

    print("-" * 70)

    metrics = [
        "retrieval_precision",
        "retrieval_recall",
        "faithfulness",
        "correctness"
    ]

    for metric in metrics:
        score_a = scores_a[metric]
        score_b = scores_b[metric]

        if score_a > score_b:
            winner = config_a
        elif score_b > score_a:
            winner = config_b
        else:
            winner = "Tie"

        print(
            f"{metric:<25}"
            f"{score_a:<15.3f}"
            f"{score_b:<15.3f}"
            f"{winner:<15}"
        )


def create_summary(results):
    summary = []

    for result in results:
        config = result["configuration"]

        summary.append({
            "experiment": config["experiment"],
            "configuration": config["config_name"],
            "chunk_size": config["chunk_size"],
            "overlap": config["overlap"],
            "top_k": config["top_k"],
            "embedding_model": config["embedding_model"],
            **result["aggregate_scores"]
        })

    return summary


if __name__ == "__main__":
    loaded_results = {}

    for path in RESULT_FILES:
        if not os.path.exists(path):
            print(f"Missing result file: {path}")
            continue

        result = load_results(path)

        config_name = result["configuration"]["config_name"]

        loaded_results[config_name] = result

    print("\nRAG EVALUATION COMPARISON")

    if "chunk_small" in loaded_results and "chunk_large" in loaded_results:
        print_experiment(
            "Experiment 1: Chunk Size",
            loaded_results["chunk_small"],
            loaded_results["chunk_large"]
        )

    if "topk_2" in loaded_results and "topk_5" in loaded_results:
        print_experiment(
            "Experiment 2: Top-k",
            loaded_results["topk_2"],
            loaded_results["topk_5"]
        )

    if "embed_minilm" in loaded_results and "embed_mpnet" in loaded_results:
        print_experiment(
            "Experiment 3: Embedding Model",
            loaded_results["embed_minilm"],
            loaded_results["embed_mpnet"]
        )
    if "final_combined" in loaded_results:
        final_scores = loaded_results["final_combined"]["aggregate_scores"]

        print("\n" + "=" * 70)
        print("Final Combined Configuration")
        print("=" * 70)

        print("Configuration: final_combined")
        print(
            f"Chunk size: {loaded_results['final_combined']['configuration']['chunk_size']}"
        )
        print(
            f"Overlap: {loaded_results['final_combined']['configuration']['overlap']}"
        )
        print(
            f"Top-k: {loaded_results['final_combined']['configuration']['top_k']}"
        )
        print(
            f"Embedding: {loaded_results['final_combined']['configuration']['embedding_model']}"
        )

        print("\nAggregate scores:")

        for metric, score in final_scores.items():
            print(f"{metric}: {score:.3f}")

    summary = create_summary(
        list(loaded_results.values())
    )

    with open(
        "results/comparison_summary.json",
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            summary,
            file,
            indent=2,
            ensure_ascii=False
        )

    print("\n" + "=" * 70)
    print("Saved: results/comparison_summary.json")
    print("=" * 70)