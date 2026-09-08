import glob
import json
import os


RESULTS_DIR = "results"
SUMMARY_PATH = os.path.join(RESULTS_DIR, "comparison_summary.json")

METRICS = [
    "document_precision",
    "document_recall",
    "context_precision",
    "context_recall",
    "faithfulness",
    "correctness",
    "ragas_style_composite",
]

METRIC_LABELS = {
    "document_precision": "Document Precision",
    "document_recall": "Document Recall",
    "context_precision": "Context Precision",
    "context_recall": "Context Recall",
    "faithfulness": "Faithfulness",
    "correctness": "Correctness",
    "ragas_style_composite": "Composite",
}

# Controlled experiments.
# Each pair changes only one retrieval variable.
EXPERIMENTS = [
    {
        "title": "Experiment 1: Chunk Size",
        "config_a": "chunk_small",
        "config_b": "chunk_large",
    },
    {
        "title": "Experiment 2: Top-k",
        "config_a": "topk_2",
        "config_b": "topk_5",
    },
    {
        "title": "Experiment 3: Embedding Model",
        "config_a": "embed_minilm",
        "config_b": "embed_mpnet",
    },
]


def load_json(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def is_valid_result(result):
    """
    Validate the newer evaluation result format.

    Older result files in the repository used a list-based format,
    so they are ignored automatically.
    """
    if not isinstance(result, dict):
        return False

    if "configuration" not in result:
        return False

    if "aggregate_scores" not in result:
        return False

    configuration = result["configuration"]
    scores = result["aggregate_scores"]

    if not isinstance(configuration, dict):
        return False

    if not isinstance(scores, dict):
        return False

    if "config_name" not in configuration:
        return False

    return True


def load_all_results():
    """
    Load all compatible *_results.json files from the results directory.
    """
    pattern = os.path.join(
        RESULTS_DIR,
        "*_results.json",
    )

    result_files = sorted(glob.glob(pattern))
    loaded_results = []

    for path in result_files:
        try:
            result = load_json(path)

            if not is_valid_result(result):
                print(
                    f"Skipping {path}: "
                    "not in the current result format."
                )
                continue

            loaded_results.append(result)

        except (
            json.JSONDecodeError,
            OSError,
        ) as error:
            print(
                f"Skipping {path}: {error}"
            )

    return loaded_results


def print_all_results(results):
    print("\n" + "=" * 112)
    print("FINAL RAG EVALUATION MATRIX")
    print("=" * 112)

    print(
        f"{'Configuration':<20}"
        f"{'Doc P':>10}"
        f"{'Doc R':>10}"
        f"{'Ctx P':>10}"
        f"{'Ctx R':>10}"
        f"{'Faith.':>10}"
        f"{'Correct.':>10}"
        f"{'Composite':>12}"
    )

    print("-" * 112)

    for result in results:
        config_name = (
            result["configuration"]["config_name"]
        )

        scores = result["aggregate_scores"]

        print(
            f"{config_name:<20}"
            f"{scores.get('document_precision', 0):>10.3f}"
            f"{scores.get('document_recall', 0):>10.3f}"
            f"{scores.get('context_precision', 0):>10.3f}"
            f"{scores.get('context_recall', 0):>10.3f}"
            f"{scores.get('faithfulness', 0):>10.3f}"
            f"{scores.get('correctness', 0):>10.3f}"
            f"{scores.get('ragas_style_composite', 0):>12.3f}"
        )


def print_experiment(
    title,
    result_a,
    result_b,
):
    scores_a = result_a["aggregate_scores"]
    scores_b = result_b["aggregate_scores"]

    name_a = (
        result_a["configuration"]["config_name"]
    )
    name_b = (
        result_b["configuration"]["config_name"]
    )

    print("\n" + "=" * 100)
    print(title)
    print("=" * 100)

    print(
        f"{'Metric':<28}"
        f"{name_a:>15}"
        f"{name_b:>15}"
        f"{'Delta':>15}"
        f"{'Winner':>20}"
    )

    print("-" * 100)

    for metric in METRICS:
        score_a = scores_a.get(metric, 0)
        score_b = scores_b.get(metric, 0)

        delta = score_b - score_a

        if score_a > score_b:
            winner = name_a

        elif score_b > score_a:
            winner = name_b

        else:
            winner = "Tie"

        print(
            f"{METRIC_LABELS[metric]:<28}"
            f"{score_a:>15.3f}"
            f"{score_b:>15.3f}"
            f"{delta:>+15.3f}"
            f"{winner:>20}"
        )


def print_controlled_experiments(
    results_by_name,
):
    print("\n" + "=" * 100)
    print("CONTROLLED EXPERIMENT COMPARISONS")
    print("=" * 100)

    for experiment in EXPERIMENTS:
        name_a = experiment["config_a"]
        name_b = experiment["config_b"]

        if (
            name_a not in results_by_name
            or name_b not in results_by_name
        ):
            print(
                f"\nSkipping {experiment['title']}: "
                "one or more configurations are missing."
            )
            continue

        print_experiment(
            experiment["title"],
            results_by_name[name_a],
            results_by_name[name_b],
        )


def print_best_configuration(results):
    best = max(
        results,
        key=lambda result: (
            result["aggregate_scores"].get(
                "ragas_style_composite",
                0,
            )
        ),
    )

    config = best["configuration"]
    scores = best["aggregate_scores"]

    print("\n" + "=" * 100)
    print("BEST CONFIGURATION")
    print("=" * 100)

    print(
        f"Configuration : "
        f"{config['config_name']}"
    )

    print(
        f"Chunk size    : "
        f"{config['chunk_size']}"
    )

    print(
        f"Overlap       : "
        f"{config['overlap']}"
    )

    print(
        f"Top-k         : "
        f"{config['top_k']}"
    )

    print(
        f"Embedding     : "
        f"{config['embedding_model']}"
    )

    print("\nScores")

    for metric in METRICS:
        print(
            f"{METRIC_LABELS[metric]:<25}: "
            f"{scores.get(metric, 0):.3f}"
        )


def create_summary(results):
    """
    Create a dashboard-friendly summary containing
    configuration parameters and aggregate metrics.
    """
    summary = []

    for result in results:
        config = result["configuration"]
        scores = result["aggregate_scores"]

        row = {
            "experiment": config.get(
                "experiment"
            ),
            "configuration": config.get(
                "config_name"
            ),
            "chunk_size": config.get(
                "chunk_size"
            ),
            "overlap": config.get(
                "overlap"
            ),
            "top_k": config.get(
                "top_k"
            ),
            "embedding_model": config.get(
                "embedding_model"
            ),
        }

        for metric in METRICS:
            row[metric] = scores.get(
                metric,
                0,
            )

        summary.append(row)

    return summary


def save_summary(summary):
    os.makedirs(
        RESULTS_DIR,
        exist_ok=True,
    )

    with open(
        SUMMARY_PATH,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            summary,
            file,
            indent=2,
            ensure_ascii=False,
        )

    print("\n" + "=" * 100)
    print(
        f"Saved comparison summary: "
        f"{SUMMARY_PATH}"
    )
    print("=" * 100)


def main():
    results = load_all_results()

    if not results:
        print(
            "No compatible evaluation "
            "result files were found."
        )
        raise SystemExit(1)

    # Keep output deterministic and easy to read.
    results = sorted(
        results,
        key=lambda result: (
            result["configuration"][
                "config_name"
            ]
        ),
    )

    results_by_name = {
        result["configuration"]["config_name"]:
        result
        for result in results
    }

    # 1. Overall evaluation matrix
    print_all_results(results)

    # 2. Controlled A/B experiments
    print_controlled_experiments(
        results_by_name
    )

    # 3. Best end-to-end configuration
    print_best_configuration(results)

    # 4. Save compact summary for dashboard
    summary = create_summary(results)
    save_summary(summary)


if __name__ == "__main__":
    main()
