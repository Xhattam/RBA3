from langchain_qwq import ChatQwen
from config import settings

import random
import time
from typing import Any

import httpx
from openai._exceptions import APIConnectionError


def get_qwen_llm():
    """ Instantiates a Qwen chat model """
    llm = ChatQwen(
        model=settings.qwen_model_name,
        temperature=0,
        api_key=settings.hf_token.get_secret_value(),
        base_url=settings.hf_api_url
    )

    return llm


def _is_transient_error(exc: Exception) -> bool:
    transient_types = (
        httpx.ReadError,
        httpx.ConnectError,
        httpx.TimeoutException,
        httpx.NetworkError,
        APIConnectionError
    )
    current: BaseException | None = exc
    seen: set[int] = set()

    while current is not None and id(current) not in seen:
        seen.add(id(current))

        if isinstance(current, transient_types):
            return True

        msg = str(current).lower()
        transient_markers = (
            "winerror 10053",
            "connection reset",
            "connection aborted",
            "read error",
            "timed out",
            "temporarily unavailable",
            "remote host closed",
            "connection error"  # openai specific
        )

        if any(marker in msg for marker in transient_markers):
            return True

        current = getattr(current, "__cause__", None) or getattr(current, "__context__", None)

    return False

def invoke_qwen_with_retry(
        structured_llm: ChatQwen,
        messages: Any,
        *,
        max_attempts: int = 5,
        base_delay_seconds: float = 1.0,
        max_delay_seconds: float = 8.0
):

    if max_attempts < 1:
        raise ValueError("max_attempts must be at least 1")

    last_exc : Exception | None = None

    for attempt in range(1, max_attempts + 1):
       try:
           return structured_llm.invoke(messages)
       except Exception as exc:
           last_exc = exc
           is_transient = _is_transient_error(exc)
           is_last_retry = attempt == max_attempts

           if (not is_transient) or is_last_retry:
               raise

           backoff = min(base_delay_seconds * (2 ** (attempt - 1)), max_delay_seconds)
           jitter = random.uniform(0.0, 0.3)
           time.sleep(backoff + jitter)

    if last_exc is not None:
        raise last_exc

    raise RuntimeError("qwen_retry_with_jitter failed without capturing an exception")





qwen_llm = get_qwen_llm()
