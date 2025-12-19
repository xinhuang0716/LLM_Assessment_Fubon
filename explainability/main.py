import asyncio
import warnings
from datetime import datetime
from pathlib import Path
import json
from core.common.clients import AsyncAzureOAIClient, AsyncGeminiClient, AsyncLlamaClient
from core.common.paths import data_dir
from core.pipelines import run_all
from core.evaluators import ScoreAggregator, ResultProcessor

async def main():
    azure_endpoint = "https://oai-ftw-jpe-sit-sandbox-01.openai.azure.com/"
    api_version = "2024-12-01-preview"

    cot_answer_llm = AsyncAzureOAIClient(
        api_key="AOAI_API_KEY",
        azure_endpoint=azure_endpoint,
        api_version=api_version,
        model="gpt-4o"
    )

    cite_answer_llm = AsyncLlamaClient(
        model='llama3.1:8b',
        temperature=0.3,
    )

    cite_judge_llm = AsyncGeminiClient(
        api_key="GEMINI_API_KEY",
        model="gemini-2.5-flash",
        temperature=0.0
    )

    try:
        reports = await run_all(
            gsm8k_path=str(data_dir() / "gsm8k.parquet"),
            nq_path=str(data_dir() / "nq.parquet"),
            cot_answer_llm=cot_answer_llm,
            cite_answer_llm=cite_answer_llm,
            cite_judge_llm=cite_judge_llm,
            cot_sample_method="random",
            cot_n_samples=30,
            cot_random_state= 50,
            citation_sample_method="random",
            citation_n_samples=5,
            citation_random_state = 50,
        )

        processor = ResultProcessor()
        success_records, failed_results, cot_scores, citation_scores = processor.process_reports(reports)

        
        aggregator = ScoreAggregator()
        task_scores = aggregator.aggregate_scores(
            cot_scores=cot_scores,
            citation_scores=citation_scores,
        )
           
        output_dir = Path(__file__).parent / "outputs"
        output_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file_success_records = output_dir / f'SUCCESS_RECORDS_{timestamp}.json'
        output_file_failed_records = output_dir / f'FAILED_RECORDS_{timestamp}.json'
        output_file_score = output_dir / f'FINAL_RESULTS_{timestamp}.json'
        
        with open(output_file_success_records, 'w', encoding='utf-8') as f:
            json.dump(success_records, f, ensure_ascii=False, indent=2)
        
        with open(output_file_failed_records, 'w', encoding='utf-8') as f:
            json.dump(failed_results, f, ensure_ascii=False, indent=2)
        
        with open(output_file_score, 'w', encoding='utf-8') as f:
            json.dump(task_scores, f, ensure_ascii=False, indent=2)

    finally:
        await cite_judge_llm.aclose()
        await cot_answer_llm.aclose()
        await cite_answer_llm.aclose()

if __name__ == "__main__":
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    asyncio.run(main())

