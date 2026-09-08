import json
import os
import time

from .rag_pipeline import RAGPipeline
from .evaluators.retrieval import evaluate_retrieval
from .evaluators.llm_judge import LLMJudge
from .evaluators.context import (
    ContextJudge,
    calculate_context_precision
)


CHECKPOINT_DIR = "results/checkpoints"


def load_questions(path="data/eval_questions.json"):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_json(path, data):
    os.makedirs(
        os.path.dirname(path) or ".",
        exist_ok=True
    )

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            data,
            file,
            indent=2,
            ensure_ascii=False
        )


def load_json(path):
    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


def is_retryable_error(error):
    """
    Retry temporary API/service failures.
    """

    message = str(error).lower()

    retryable_terms = [
        "429",
        "503",
        "resource exhausted",
        "rate limit",
        "too many requests",
        "unavailable",
        "high demand",
        "temporarily"
    ]

    return any(
        term in message
        for term in retryable_terms
    )


def call_with_retry(
    function,
    max_attempts=4,
    initial_delay=8
):
    """
    Execute an LLM-dependent function with exponential backoff
    for transient failures.
    """

    delay = initial_delay

    for attempt in range(1, max_attempts + 1):

        try:
            return function()

        except Exception as error:

            if not is_retryable_error(error):
                raise

            if attempt == max_attempts:
                raise

            print(
                f"  Temporary API error. "
                f"Retrying in {delay}s "
                f"(attempt {attempt}/{max_attempts})..."
            )

            time.sleep(delay)
            delay *= 2


def evaluate_pipeline(
    top_k=3,
    collection_name="rag_documents",
    embedding_model="sentence-transformers/all-MiniLM-L6-v2",
    checkpoint_name=None,
    resume=True
):
    questions = load_questions()

    rag = RAGPipeline(
        top_k=top_k,
        collection_name=collection_name,
        embedding_model=embedding_model
    )

    judge = LLMJudge()
    context_judge = ContextJudge()

    results = []

    checkpoint_path = None

    if checkpoint_name:
        checkpoint_path = os.path.join(
            CHECKPOINT_DIR,
            f"{checkpoint_name}_checkpoint.json"
        )

    # --------------------------------------------------
    # Resume previous checkpoint if available
    # --------------------------------------------------

    if (
        resume
        and checkpoint_path
        and os.path.exists(checkpoint_path)
    ):
        checkpoint = load_json(
            checkpoint_path
        )

        results = checkpoint.get(
            "results",
            []
        )

        completed_ids = {
            result["id"]
            for result in results
        }

        print(
            f"\nResuming from checkpoint: "
            f"{len(results)}/{len(questions)} questions completed."
        )

    else:
        completed_ids = set()

    # --------------------------------------------------
    # Evaluate questions
    # --------------------------------------------------

    for question_data in questions:

        question_id = question_data["id"]

        if question_id in completed_ids:
            print(
                f"Skipping {question_id}: "
                f"already completed."
            )
            continue

        question = question_data["question"]
        expected_answer = (
            question_data["expected_answer"]
        )

        print(
            f"\nEvaluating {question_id}: "
            f"{question}"
        )

        # --------------------------------------------------
        # RAG generation
        # --------------------------------------------------

        rag_result = call_with_retry(
            lambda: rag.answer(question)
        )

        retrieved_chunks = (
            rag_result["retrieved_chunks"]
        )

        context = "\n\n".join(
            chunk["text"]
            for chunk in retrieved_chunks
        )

        # --------------------------------------------------
        # Document-level retrieval
        # --------------------------------------------------

        retrieval_score = evaluate_retrieval(
            retrieved_chunks,
            question_data["relevant_sources"]
        )

        document_precision = (
            retrieval_score["precision"]
        )

        document_recall = (
            retrieval_score["recall"]
        )

        # --------------------------------------------------
        # Context Precision + Context Recall
        # One LLM call for both
        # --------------------------------------------------

        print(
            "  Evaluating context precision/recall..."
        )

        context_result = call_with_retry(
            lambda: context_judge.evaluate_context(
                question=question,
                reference_answer=expected_answer,
                retrieved_chunks=retrieved_chunks
            )
        )

        # Convert chunk judgments into the format
        # expected by calculate_context_precision()
        context_chunk_results = []

        for judgment in context_result[
            "chunk_judgments"
        ]:

            rank = int(
                judgment["rank"]
            )

            if rank < 1 or rank > len(
                retrieved_chunks
            ):
                raise ValueError(
                    f"Invalid chunk rank returned by "
                    f"LLM: {rank}"
                )

            chunk = retrieved_chunks[
                rank - 1
            ]

            context_chunk_results.append({
                "rank": rank,
                "chunk_id": chunk["chunk_id"],
                "document_id": chunk["document_id"],
                "relevant": int(
                    judgment["relevant"]
                ),
                "reason": judgment["reason"]
            })

        context_precision = (
            calculate_context_precision(
                context_chunk_results
            )
        )

        context_recall = context_result[
            "context_recall"
        ]

        context_recall_claims = (
            context_result["claims"]
        )

        # --------------------------------------------------
        # Faithfulness + Correctness
        # --------------------------------------------------

        print(
            "  Evaluating "
            "answer faithfulness/correctness..."
        )

        time.sleep(4)

        judge_score = call_with_retry(
            lambda: judge.evaluate(
                question=question,
                expected_answer=expected_answer,
                generated_answer=rag_result["answer"],
                context=context
            )
        )

        time.sleep(4)

        faithfulness = judge_score[
            "faithfulness"
        ]

        correctness = judge_score[
            "correctness"
        ]

        # --------------------------------------------------
        # RAGAS-style composite
        # --------------------------------------------------

        ragas_style_composite = (
            context_precision
            + context_recall
            + faithfulness
            + correctness
        ) / 4

        # --------------------------------------------------
        # Build result
        # --------------------------------------------------

        result = {
            "id": question_id,
            "type": question_data["type"],
            "question": question,
            "expected_answer": expected_answer,
            "generated_answer": rag_result["answer"],

            "relevant_sources": (
                question_data["relevant_sources"]
            ),

            "retrieved_documents": [
                chunk["document_id"]
                for chunk in retrieved_chunks
            ],

            "retrieved_chunks": [
                {
                    "chunk_id": chunk["chunk_id"],
                    "document_id": chunk["document_id"],
                    "distance": chunk["distance"],
                    "text": chunk["text"]
                }
                for chunk in retrieved_chunks
            ],

            # Source-level retrieval metrics
            "document_precision": (
                document_precision
            ),

            "document_recall": (
                document_recall
            ),

            # Context-level retrieval metrics
            "context_precision": (
                context_precision
            ),

            "context_recall": (
                context_recall
            ),

            # Auditable context judgments
            "context_chunk_judgments": (
                context_chunk_results
            ),

            "context_recall_claims": (
                context_recall_claims
            ),

            # Generation metrics
            "faithfulness": faithfulness,

            "correctness": correctness,

            # Overall project metric
            "ragas_style_composite": (
                ragas_style_composite
            )
        }

        results.append(result)
        completed_ids.add(question_id)

        # --------------------------------------------------
        # Save checkpoint immediately
        # --------------------------------------------------

        if checkpoint_path:

            save_json(
                checkpoint_path,
                {
                    "configuration": {
                        "top_k": top_k,
                        "collection_name": (
                            collection_name
                        ),
                        "embedding_model": (
                            embedding_model
                        )
                    },

                    "completed_questions": (
                        len(results)
                    ),

                    "total_questions": (
                        len(questions)
                    ),

                    "results": results
                }
            )

            print(
                f"  Checkpoint saved "
                f"({len(results)}/{len(questions)})."
            )

    return results


def calculate_aggregate_scores(results):

    if not results:
        return {
            "document_precision": 0,
            "document_recall": 0,
            "context_precision": 0,
            "context_recall": 0,
            "faithfulness": 0,
            "correctness": 0,
            "ragas_style_composite": 0
        }

    return {
        "document_precision": (
            sum(
                result["document_precision"]
                for result in results
            ) / len(results)
        ),

        "document_recall": (
            sum(
                result["document_recall"]
                for result in results
            ) / len(results)
        ),

        "context_precision": (
            sum(
                result["context_precision"]
                for result in results
            ) / len(results)
        ),

        "context_recall": (
            sum(
                result["context_recall"]
                for result in results
            ) / len(results)
        ),

        "faithfulness": (
            sum(
                result["faithfulness"]
                for result in results
            ) / len(results)
        ),

        "correctness": (
            sum(
                result["correctness"]
                for result in results
            ) / len(results)
        ),

        "ragas_style_composite": (
            sum(
                result["ragas_style_composite"]
                for result in results
            ) / len(results)
        )
    }


def calculate_scores_by_type(results):

    scores = {}

    for result in results:

        query_type = result["type"]

        scores.setdefault(
            query_type,
            []
        ).append(result)

    output = {}

    for query_type, type_results in scores.items():

        count = len(type_results)

        output[query_type] = {
            "count": count,

            "document_precision": (
                sum(
                    result["document_precision"]
                    for result in type_results
                ) / count
            ),

            "document_recall": (
                sum(
                    result["document_recall"]
                    for result in type_results
                ) / count
            ),

            "context_precision": (
                sum(
                    result["context_precision"]
                    for result in type_results
                ) / count
            ),

            "context_recall": (
                sum(
                    result["context_recall"]
                    for result in type_results
                ) / count
            ),

            "faithfulness": (
                sum(
                    result["faithfulness"]
                    for result in type_results
                ) / count
            ),

            "correctness": (
                sum(
                    result["correctness"]
                    for result in type_results
                ) / count
            ),

            "ragas_style_composite": (
                sum(
                    result["ragas_style_composite"]
                    for result in type_results
                ) / count
            )
        }

    return output


if __name__ == "__main__":
    import sys

    config_path = sys.argv[1]

    with open(
        config_path,
        "r",
        encoding="utf-8"
    ) as file:
        config = json.load(file)

    if config["experiment"] == "top_k":
        collection_name = "rag_chunk_small"
    else:
        collection_name = (
            f"rag_{config['config_name']}"
        )

    print("\n" + "=" * 70)
    print(
        f"Running configuration: "
        f"{config['config_name']}"
    )
    print("=" * 70)

    print(
        f"Experiment: {config['experiment']}"
    )

    print(
        f"Chunk size: {config['chunk_size']}"
    )

    print(
        f"Overlap: {config['overlap']}"
    )

    print(
        f"Top-k: {config['top_k']}"
    )

    print(
        f"Embedding: {config['embedding_model']}"
    )

    results = evaluate_pipeline(
        top_k=config["top_k"],
        collection_name=collection_name,
        embedding_model=config["embedding_model"],
        checkpoint_name=config["config_name"],
        resume=True
    )

    aggregate = calculate_aggregate_scores(
        results
    )

    by_type = calculate_scores_by_type(
        results
    )

    output = {
        "configuration": config,
        "aggregate_scores": aggregate,
        "scores_by_type": by_type,
        "results": results
    }

    os.makedirs(
        "results",
        exist_ok=True
    )

    output_path = (
        f"results/"
        f"{config['config_name']}_results.json"
    )

    save_json(
        output_path,
        output
    )

    print("\n" + "=" * 70)
    print("AGGREGATE SCORES")
    print("=" * 70)

    for metric, score in aggregate.items():

        print(
            f"{metric:<28}: "
            f"{score:.3f}"
        )

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
                f"  {metric:<26}: "
                f"{score:.3f}"
            )

    print("\n" + "=" * 70)
    print(
        f"Saved: {output_path}"
    )
    print("=" * 70)