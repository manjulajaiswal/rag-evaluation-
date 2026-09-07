import json
import sys
import os

from src.evaluation import (
    evaluate_pipeline,
    calculate_aggregate_scores,
    calculate_scores_by_type
)


def load_config(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


if __name__ == "__main__":
    config_path = sys.argv[1]

    config = load_config(config_path)

    if config["experiment"] == "top_k":
        collection_name = "rag_chunk_small"
    else:
        collection_name = f"rag_{config['config_name']}"

    print("\n" + "=" * 60)
    print(f"Running configuration: {config['config_name']}")
    print("=" * 60)

    results = evaluate_pipeline(
        top_k=config["top_k"],
        collection_name=collection_name,
        embedding_model=config["embedding_model"]
    )

    aggregate = calculate_aggregate_scores(results)
    by_type = calculate_scores_by_type(results)

    output = {
        "configuration": config,
        "aggregate_scores": aggregate,
        "scores_by_type": by_type,
        "results": results
    }

    os.makedirs("results", exist_ok=True)

    output_path = (
        f"results/{config['config_name']}_results.json"
    )

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(
            output,
            file,
            indent=2,
            ensure_ascii=False
        )

    print(f"\nResults saved to: {output_path}")

    print("\nAggregate scores:")

    for metric, score in aggregate.items():
        print(f"{metric}: {score:.3f}")

    print("\nScores by query type:")

    for query_type, scores in by_type.items():
        print(f"\n{query_type} ({scores['count']} questions)")

        for metric, score in scores.items():
            if metric != "count":
                print(f"  {metric}: {score:.3f}")