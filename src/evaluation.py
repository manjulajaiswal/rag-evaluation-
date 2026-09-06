import json
import time

from .rag_pipeline import RAGPipeline
from .evaluators.retrieval import evaluate_retrieval
from .evaluators.llm_judge import LLMJudge


def load_questions(path="data/eval_questions.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def evaluate_pipeline(top_k=3, collection_name="rag_documents"):
    questions = load_questions()

    rag = RAGPipeline(
        top_k=top_k,
        collection_name=collection_name
    )
    judge = LLMJudge()

    results = []

    for question_data in questions:
        question = question_data["question"]
        expected_answer = question_data["expected_answer"]
        relevant_source = question_data["relevant_source"]

        rag_result = rag.answer(question)

        time.sleep(4)

        retrieved_chunks = rag_result["retrieved_chunks"]
        generated_answer = rag_result["answer"]

        context = "\n\n".join(
            chunk["text"]
            for chunk in retrieved_chunks
        )

        retrieval_score = evaluate_retrieval(
            retrieved_chunks,
            relevant_source
        )

        judge_score = judge.evaluate(
            question,
            expected_answer,
            generated_answer,
            context
        )

        time.sleep(4)

        results.append({
            "id": question_data["id"],
            "question": question,
            "expected_answer": expected_answer,
            "generated_answer": generated_answer,
            "relevant_source": relevant_source,
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
    total = len(results)

    if total == 0:
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
        ) / total,

        "retrieval_recall": sum(
            result["retrieval_recall"]
            for result in results
        ) / total,

        "faithfulness": sum(
            result["faithfulness"]
            for result in results
        ) / total,

        "correctness": sum(
            result["correctness"]
            for result in results
        ) / total
    }