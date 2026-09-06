import json


def load_results(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def calculate_aggregate(results):
    total = len(results)

    return {
        "retrieval_precision": sum(
            r["retrieval_precision"] for r in results
        ) / total,

        "retrieval_recall": sum(
            r["retrieval_recall"] for r in results
        ) / total,

        "faithfulness": sum(
            r["faithfulness"] for r in results
        ) / total,

        "correctness": sum(
            r["correctness"] for r in results
        ) / total
    }


def main():
    config_a = load_results("results/config_a_results.json")
    config_b = load_results("results/config_b_results.json")

    aggregate_a = calculate_aggregate(config_a)
    aggregate_b = calculate_aggregate(config_b)

    print("\nCONFIGURATION COMPARISON")
    print("=" * 70)

    print(
        f"{'Metric':<25}"
        f"{'Config A':>15}"
        f"{'Config B':>15}"
        f"{'Winner':>15}"
    )

    print("-" * 70)

    metrics = [
        "retrieval_precision",
        "retrieval_recall",
        "faithfulness",
        "correctness"
    ]

    for metric in metrics:
        a = aggregate_a[metric]
        b = aggregate_b[metric]

        if a > b:
            winner = "Config A"
        elif b > a:
            winner = "Config B"
        else:
            winner = "Tie"

        print(
            f"{metric:<25}"
            f"{a:>14.2%}"
            f"{b:>14.2%}"
            f"{winner:>15}"
        )

    print("\nPER-QUESTION RETRIEVAL COMPARISON")
    print("=" * 90)

    print(
        f"{'Question':<12}"
        f"{'A Precision':>15}"
        f"{'B Precision':>15}"
        f"{'A Recall':>12}"
        f"{'B Recall':>12}"
    )

    print("-" * 90)

    for a, b in zip(config_a, config_b):
        print(
            f"{a['id']:<12}"
            f"{a['retrieval_precision']:>14.2%}"
            f"{b['retrieval_precision']:>14.2%}"
            f"{a['retrieval_recall']:>11.2%}"
            f"{b['retrieval_recall']:>11.2%}"
        )


if __name__ == "__main__":
    main()