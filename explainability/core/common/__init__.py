"""
Common Module - Shared utilities and infrastructure.

Provides common utilities for:
- Batch processing with async concurrency control
- LLM client interfaces (Azure OpenAI, Gemini)
- File path management
"""

from . import batch
from . import clients

__all__ = ["batch", "clients"]
