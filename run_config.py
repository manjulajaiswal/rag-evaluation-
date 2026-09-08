import json
import os
import sys

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

    print("\n" + "=" * 70)
    print(f"Running configuration: {config['config_name']}")
    print("=" * 70)

    print(f"Experiment: {config['experiment']}")
    print(f"Chunk size: {config['chunk_size']}")
    print(f"Overlap: {config['overlap']}")
    print(f"Top-k: {config['top_k']}")
    print(f"Embedding: {config['embedding_model']}")
    print("=" * 70)

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

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            output,
            file,
            indent=2,
            ensure_ascii=False
        )

    print("\n" + "=" * 70)
    print("AGGREGATE SCORES")
    print("=" * 70)

    for metric, score in aggregate.items():
        print(f"{metric:<28}: {score:.3f}")

    print("\n" + "=" * 70)
    print("SCORES BY QUERY TYPE")
    print("=" * 70)

    for query_type, scores in by_type.items():

        print(
            f"\n{query_type} "
            f"({scores['count']} questions)"
        )

        for metric, score in scores.items():

            if metric == "count":
                continue

            print(
                f"  {metric:<26}: {score:.3f}"
            )

    print("\n" + "=" * 70)
    print(f"Saved: {output_path}")
    print("=" * 70)