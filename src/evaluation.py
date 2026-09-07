import json
import time

from .rag_pipeline import RAGPipeline
from .evaluators.retrieval import evaluate_retrieval
from .evaluators.llm_judge import LLMJudge


def load_questions(path="data/eval_questions.json"):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def evaluate_pipeline(
    top_k=3,
    collection_name="rag_documents",
    embedding_model="sentence-transformers/all-MiniLM-L6-v2"
):
    questions = load_questions()

    rag = RAGPipeline(
    top_k=top_k,
    collection_name=collection_name,
    embedding_model=embedding_model
)

    judge = LLMJudge()

    results = []

    for question_data in questions:
        question = question_data["question"]

        print(f"Evaluating {question_data['id']}: {question}")

        rag_result = rag.answer(question)

        retrieved_chunks = rag_result["retrieved_chunks"]

        context = "\n\n".join(
            chunk["text"]
            for chunk in retrieved_chunks
        )

        time.sleep(4)

        retrieval_score = evaluate_retrieval(
            retrieved_chunks,
            question_data["relevant_sources"]
        )

        judge_score = judge.evaluate(
            question=question,
            expected_answer=question_data["expected_answer"],
            generated_answer=rag_result["answer"],
            context=context
        )

        time.sleep(4)

        results.append({
            "id": question_data["id"],
            "type": question_data["type"],
            "question": question,
            "expected_answer": question_data["expected_answer"],
            "generated_answer": rag_result["answer"],
            "relevant_sources": question_data["relevant_sources"],
            "retrieved_documents": [
                chunk["document_id"]
                for chunk in retrieved_chunks
            ],
            "retrieval_precision": retrieval_score["precision"],
            "retrieval_recall": retrieval_score["recall"],
            "faithfulness": judge_score["faithfulness"],
            "correctness": judge_score["correctness"]
        })

    return results


def calculate_aggregate_scores(results):
    if not results:
        return {
            "retrieval_precision": 0,
            "retrieval_recall": 0,
            "faithfulness": 0,
            "correctness": 0
        }

    return {
        "retrieval_precision": sum(
            result["retrieval_precision"]
            for result in results
        ) / len(results),

        "retrieval_recall": sum(
            result["retrieval_recall"]
            for result in results
        ) / len(results),

        "faithfulness": sum(
            result["faithfulness"]
            for result in results
        ) / len(results),

        "correctness": sum(
            result["correctness"]
            for result in results
        ) / len(results)
    }


def calculate_scores_by_type(results):
    scores = {}

    for result in results:
        query_type = result["type"]

        if query_type not in scores:
            scores[query_type] = []

        scores[query_type].append(result)

    output = {}

    for query_type, type_results in scores.items():
        output[query_type] = {
            "count": len(type_results),

            "retrieval_precision": sum(
                r["retrieval_precision"]
                for r in type_results
            ) / len(type_results),

            "retrieval_recall": sum(
                r["retrieval_recall"]
                for r in type_results
            ) / len(type_results),

            "faithfulness": sum(
                r["faithfulness"]
                for r in type_results
            ) / len(type_results),

            "correctness": sum(
                r["correctness"]
                for r in type_results
            ) / len(type_results)
        }

    return output