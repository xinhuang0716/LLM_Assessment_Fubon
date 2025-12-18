import asyncio
from datetime import datetime
from typing import Dict, Any, List, Optional
import pandas as pd

class AsyncBatchRunner:
    """
    Asynchronously runs batch evaluations with concurrency control and flexible sampling.
    """
    
    def __init__(self, df: pd.DataFrame, evaluator, max_concurrent: int = 3, random_state: int = 0):
        """
        Initialize AsyncBatchRunner with dataset and evaluator configuration.
        
        Args:
            df: Pandas DataFrame containing the data to be evaluated.
            evaluator: Evaluator object with async run_one(qid, row) method.
            max_concurrent: Maximum number of concurrent evaluations (default: 3).
            random_state: Random seed for reproducible sampling (default: 0).
        """
        self.df = df
        self.evaluator = evaluator
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.random_state = random_state

    def sample(self, method: str = "random", n: int = 10, indices: Optional[List[int]] = None) -> pd.DataFrame:
        """
        Sample rows from the dataset using specified sampling method.
        
        Supports three sampling strategies:
        - "fixed": Select specific rows by indices
        - "first": Take the first n rows in order
        - "random": Randomly sample n rows (default, uses random_state for reproducibility)
        
        The returned DataFrame includes an 'original_index' column preserving the original row indices.
        
        Args:
            method: Sampling method - "fixed", "first", or "random" (default: "random").
            n: Number of samples to take (ignored for "fixed" method).
            indices: List of specific indices to sample (only used with "fixed" method).
            
        Returns:
            Pandas DataFrame with sampled rows and added 'original_index' column.
        """
        if method == "fixed" and indices is not None:
            sampled = self.df.iloc[indices].copy()
        elif method == "first":
            sampled = self.df.head(n).copy()
        else:
            sampled = self.df.sample(n=min(n, len(self.df)), random_state=self.random_state).copy()

        sampled = sampled.reset_index(drop=False).rename(columns={"index": "original_index"})
        return sampled

    async def _one(self, idx: int, row: pd.Series) -> Dict[str, Any]:
        """
        Execute a single evaluation task with concurrency control.
        
        Uses a semaphore to enforce the max_concurrent limit, preventing resource exhaustion.
        Extracts the original index from the row and delegates to evaluator.run_one().
        
        Args:
            idx: Current iteration index in the sampled DataFrame.
            row: Pandas Series representing one data row.
            
        Returns:
            Dictionary result from evaluator.run_one() or error dictionary if evaluation fails.
        """
        async with self.semaphore:
            qid = int(row.get("original_index", idx))
            try:
                return await self.evaluator.run_one(qid=qid, row=row)
            except Exception as e:
                return {"success": False, "question_id": qid, "error": f"Runner error: {e}"}

    async def run(self, sample_method: str = "random", n_samples: int = 10, fixed_indices: Optional[List[int]] = None) -> Dict[str, Any]:
        """
        Execute batch evaluation on sampled data with concurrency control and detailed reporting.
        
        Orchestrates the entire evaluation pipeline:
        1. Samples rows from the dataset using specified method
        2. Creates async tasks for each sampled row
        3. Executes tasks concurrently (limited by max_concurrent)
        4. Separates successful and failed results
        5. Generates comprehensive metadata report
        
        Args:
            sample_method: Sampling method - "random", "first", or "fixed" (default: "random").
            n_samples: Number of samples to evaluate (default: 10).
            fixed_indices: List of specific indices (only used when sample_method="fixed").
            
        Returns:
            containing:
                - metadata: Dictionary containing:
                    - evaluator: Name of the evaluator
                    - start_time: ISO format start timestamp
                    - end_time: ISO format end timestamp
                    - duration_seconds: Total execution time in seconds
                    - total_questions: Total samples processed
                    - successful: Count of successful evaluations
                    - failed: Count of failed evaluations
                    - sample_method: The sampling method used             
                - successful_results: List of successful evaluation results
                - failed_results: List of failed evaluation results
        """
        start = datetime.now()
        sampled = self.sample(sample_method, n_samples, fixed_indices)

        tasks = [self._one(i, row) for i, row in sampled.iterrows()]
        results = await asyncio.gather(*tasks, return_exceptions=False)

        end = datetime.now()
        successful = [r for r in results if r.get("success")]
        failed = [r for r in results if not r.get("success")]

        return {
            "metadata": {
                "evaluator": getattr(self.evaluator, "name", "Unknown"),
                "start_time": start.strftime("%Y-%m-%d %H:%M:%S"),
                "end_time": end.strftime("%Y-%m-%d %H:%M:%S"),
                "duration_seconds": (end - start).total_seconds(),
                "total_questions": len(sampled),
                "successful": len(successful),
                "failed": len(failed),
                "sample_method": sample_method,
            },
            "successful_results": successful,
            "failed_results": failed,
        }
