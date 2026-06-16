"""Exception Handler Chain Pattern — structured, typed exception handling for agents.

Each handler targets a specific exception category (rate limits, bad output,
policy violations). The chain is traversed in order; first match wins.

Based on SHIELDA: arXiv:2508.07935.

Run: python3 resilience/exception_handler_chain.py
See: patterns/implementation/exception-handler-chain.md
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any, Callable, Type


class RateLimitError(Exception):
    pass


class OutputFormatError(Exception):
    pass


class PolicyViolationError(Exception):
    pass


@dataclass
class HandlerResult:
    success: bool
    value: Any = None
    handler_used: str = ""
    attempts: int = 1


class ExceptionHandler:
    def __init__(self, on: Type[Exception]) -> None:
        self.on = on

    def matches(self, exc: Exception) -> bool:
        return isinstance(exc, self.on)

    def handle(self, exc: Exception, fn: Callable, *args: Any, **kwargs: Any) -> HandlerResult:
        raise NotImplementedError


class RetryHandler(ExceptionHandler):
    def __init__(self, on: Type[Exception], max_retries: int = 3, delay: float = 0.0) -> None:
        super().__init__(on)
        self.max_retries = max_retries
        self.delay = delay

    def handle(self, exc: Exception, fn: Callable, *args: Any, **kwargs: Any) -> HandlerResult:
        for attempt in range(1, self.max_retries + 1):
            try:
                if self.delay:
                    time.sleep(self.delay)
                result = fn(*args, **kwargs)
                print(f"[retry] recovered on attempt {attempt}")
                return HandlerResult(success=True, value=result, handler_used="retry", attempts=attempt)
            except self.on as e:
                exc = e
        return HandlerResult(success=False, handler_used="retry_exhausted", attempts=self.max_retries)


class FallbackHandler(ExceptionHandler):
    def __init__(self, on: Type[Exception], fallback: Callable) -> None:
        super().__init__(on)
        self.fallback = fallback

    def handle(self, exc: Exception, fn: Callable, *args: Any, **kwargs: Any) -> HandlerResult:
        print(f"[fallback] delegating to fallback agent after {type(exc).__name__}")
        result = self.fallback(*args, **kwargs)
        return HandlerResult(success=True, value=result, handler_used="fallback")


class EscalateHandler(ExceptionHandler):
    def __init__(self, on: Type[Exception], notify: Callable[[Exception], None]) -> None:
        super().__init__(on)
        self.notify = notify

    def handle(self, exc: Exception, fn: Callable, *args: Any, **kwargs: Any) -> HandlerResult:
        print(f"[escalate] notifying human about {type(exc).__name__}: {exc}")
        self.notify(exc)
        return HandlerResult(success=False, handler_used="escalated")


class ExceptionHandlerChain:
    def __init__(self) -> None:
        self._handlers: list[ExceptionHandler] = []

    def add(self, handler: ExceptionHandler) -> "ExceptionHandlerChain":
        self._handlers.append(handler)
        return self

    def execute(self, fn: Callable, *args: Any, **kwargs: Any) -> HandlerResult:
        try:
            result = fn(*args, **kwargs)
            return HandlerResult(success=True, value=result, handler_used="none")
        except Exception as exc:
            for handler in self._handlers:
                if handler.matches(exc):
                    return handler.handle(exc, fn, *args, **kwargs)
            raise


def main() -> None:
    print("=== Exception Handler Chain Pattern ===\n")
    call_count = {"n": 0}

    def flaky_agent(query: str) -> str:
        call_count["n"] += 1
        if call_count["n"] < 3:
            raise RateLimitError("429 Too Many Requests")
        return f"answer to: {query}"

    def simple_fallback(query: str) -> str:
        return f"[fallback] simplified answer to: {query}"

    def human_notify(exc: Exception) -> None:
        print(f"  >> HUMAN ALERT: {exc}")

    chain = (
        ExceptionHandlerChain()
        .add(RetryHandler(on=RateLimitError, max_retries=3, delay=0.0))
        .add(FallbackHandler(on=OutputFormatError, fallback=simple_fallback))
        .add(EscalateHandler(on=Exception, notify=human_notify))
    )

    # Scenario 1: rate limit resolved on retry
    result = chain.execute(flaky_agent, "what is RAG?")
    print(f"Result 1: {result.value} (handler={result.handler_used}, attempts={result.attempts})\n")

    # Scenario 2: output format error → fallback
    def bad_format_agent(query: str) -> str:
        raise OutputFormatError("response was not valid JSON")

    result2 = chain.execute(bad_format_agent, "summarize document")
    print(f"Result 2: {result2.value} (handler={result2.handler_used})\n")

    # Scenario 3: policy violation → escalation
    def policy_agent(query: str) -> str:
        raise PolicyViolationError("output contains PII")

    result3 = chain.execute(policy_agent, "process user data")
    print(f"Result 3: success={result3.success}, handler={result3.handler_used}")


if __name__ == "__main__":
    main()
