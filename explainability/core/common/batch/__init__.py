"""
Batch Processing Module - Async batch evaluation runner.

Provides concurrent evaluation infrastructure:
- AsyncBatchRunner: Manages concurrent evaluations with semaphore control
- Multiple sampling strategies (random, sequential, fixed indices)
- Comprehensive metadata and result aggregation
"""

from .async_batch_runner import AsyncBatchRunner

__all__ = ["AsyncBatchRunner"]
