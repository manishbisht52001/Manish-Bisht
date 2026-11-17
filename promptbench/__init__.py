"""PromptBench: small, provider-neutral prompt evaluation primitives."""

from .dataset import load_jsonl, load_outputs_jsonl
from .evaluator import Case, EvaluationResult, evaluate, run_dataset

__all__ = [
    "Case",
    "EvaluationResult",
    "evaluate",
    "load_jsonl",
    "load_outputs_jsonl",
    "run_dataset",
]
__version__ = "0.1.0"
