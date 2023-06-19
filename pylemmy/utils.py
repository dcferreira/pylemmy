import time
from typing import Any, Callable, Generator, Iterable, Optional, TypeVar

T = TypeVar("T")


def stream_generator(
    function: Callable[..., Iterable[T]],
    unique_key_fn: Callable[[T], str],
    *,
    filter_fn: Callable[[T], bool] = lambda _: True,
    limit: Optional[int] = None,
    max_wait_time: int = 300,
    min_wait_time: int = 1,
    **function_kwargs: Any,
) -> Generator[T, None, None]:
    found_keys = set()
    count = 0
    last_key: str = ""

    wait_time = min_wait_time
    while True:
        if limit is not None and count >= limit:
            break
        first_key = last_key
        results = function(**function_kwargs)
        for r in filter(filter_fn, results):
            unique_key = unique_key_fn(r)
            if unique_key not in found_keys:
                last_key = unique_key
                yield r
                found_keys.add(unique_key)

        if first_key == last_key:  # no new results
            wait_time = min(2 * wait_time, max_wait_time)
        else:
            wait_time = min_wait_time

        time.sleep(wait_time)
        count += 1
