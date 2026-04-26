"""
Circuit breakers for downstream service calls.

Each breaker opens after FAIL_MAX consecutive failures and stays open for
RESET_TIMEOUT seconds before allowing a single probe request (half-open state).
Import the pre-built instances; do not create new ones per request.
"""

import asyncio
import functools
import logging
from typing import Callable, TypeVar, Any

import pybreaker

logger = logging.getLogger(__name__)

# ── Breaker configuration ──────────────────────────────────────────────────────
_FAIL_MAX = 5        # consecutive failures before opening
_RESET_TIMEOUT = 30  # seconds the breaker stays open before probing

# ── Per-service breakers ───────────────────────────────────────────────────────
embedding_breaker = pybreaker.CircuitBreaker(
    fail_max=_FAIL_MAX,
    reset_timeout=_RESET_TIMEOUT,
    name="embedding",
)

reranking_breaker = pybreaker.CircuitBreaker(
    fail_max=_FAIL_MAX,
    reset_timeout=_RESET_TIMEOUT,
    name="reranking",
)

chromadb_breaker = pybreaker.CircuitBreaker(
    fail_max=_FAIL_MAX,
    reset_timeout=_RESET_TIMEOUT,
    name="chromadb",
)

llm_breaker = pybreaker.CircuitBreaker(
    fail_max=_FAIL_MAX,
    reset_timeout=_RESET_TIMEOUT,
    name="llm",
)

# ── Async helper ──────────────────────────────────────────────────────────────
F = TypeVar("F")


def with_breaker(breaker: pybreaker.CircuitBreaker):
    """
    Decorator that wraps an async function with a circuit breaker.
    Raises pybreaker.CircuitBreakerError when the circuit is open.
    """
    def decorator(fn: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(fn)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            # pybreaker is synchronous; run the decorated coroutine inside it
            # by wrapping it in a sync function that drives the event loop.
            result_holder: list[Any] = []
            exc_holder: list[BaseException] = []

            @breaker
            def _sync_call() -> None:
                loop = asyncio.get_event_loop()
                try:
                    result_holder.append(loop.run_until_complete(fn(*args, **kwargs)))
                except Exception as exc:
                    exc_holder.append(exc)
                    raise

            _sync_call()

            if exc_holder:
                raise exc_holder[0]
            return result_holder[0]

        return wrapper
    return decorator
