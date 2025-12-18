import pandas as pd
from core.common.batch import AsyncBatchRunner
from core.evaluators.cot import CoTEvaluator
from core.evaluators.citation import CitationEvaluator
from core.config import CitationConfig, CoTConfig

async def run_all(gsm8k_path: str, nq_path: str, cot_answer_llm, cite_answer_llm, cite_judge_llm, cot_sample_method: str = "random", cot_n_samples: int = 30, citation_sample_method: str = "random", citation_n_samples: int = 1):
    """
    Execute both CoT and Citation evaluation pipelines with configurable sampling parameters.
    
    Args:
        gsm8k_path: Path to the GSM8K dataset for CoT evaluation.
        nq_path: Path to the NQ dataset for Citation evaluation.
        cot_answer_llm: LLM client for generating CoT answers.
        cite_answer_llm: LLM client for generating citation answers.
        cite_judge_llm: LLM client for judging citation quality.
        cot_sample_method: Sampling method for CoT dataset ("random", "sequential", etc.). Defaults to "random".
        cot_n_samples: Number of samples to evaluate for CoT. Defaults to 30.
        citation_sample_method: Sampling method for Citation dataset ("random", "sequential", etc.). Defaults to "random".
        citation_n_samples: Number of samples to evaluate for Citation. Defaults to 1.
        
    Returns:
        List of evaluation reports from both CoT and Citation evaluators.
    """
    reports = []

    # CoT
    df_gsm = pd.read_parquet(gsm8k_path)
    cot_eval = CoTEvaluator(answer_llm=cot_answer_llm, config=CoTConfig)
    cot_runner = AsyncBatchRunner(df_gsm, evaluator=cot_eval, max_concurrent=3)
    cot_report = await cot_runner.run(sample_method=cot_sample_method, n_samples=cot_n_samples)
    reports.append(cot_report)

    # Citation
    df_nq = pd.read_parquet(nq_path)
    cite_eval = CitationEvaluator(answer_llm=cite_answer_llm, judge_llm=cite_judge_llm, config=CitationConfig)
    cite_runner = AsyncBatchRunner(df_nq, evaluator=cite_eval, max_concurrent=1)
    cite_report = await cite_runner.run(sample_method=citation_sample_method, n_samples=citation_n_samples)
    reports.append(cite_report)

    return reports
