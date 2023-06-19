"""General utilities package."""
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
    """Helper function to generate streams.

    :param function: A function to call repeatedly, which outputs a list of objects.
    :param unique_key_fn: A function that takes an object and outputs a unique id.
    This is used to keep track of what results were already yielded.
    :param filter_fn: Ignore objects which return `True` for this function.
    :param limit: Maximum number of objects to yield.
    :param max_wait_time: If a function returns no new results, the time between calls
    to it increases. This sets the maximum time (in seconds) to wait before calling it
    again.
    :param min_wait_time: Minimum time (in seconds) to wait before calling the function
    again.
    :param function_kwargs: Keyword parameters that are passed to the function.
    """
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
