"""General utilities package."""
import asyncio
import time
from typing import (
    Any,
    AsyncGenerator,
    Callable,
    Generator,
    Iterable,
    Optional,
    Sequence,
    TypeVar,
)

from aiostream import stream
from mypy_extensions import KwArg

T = TypeVar("T")


def stream_generator(
    results_fn: Callable[[KwArg(Any)], Iterable[T]],
    unique_key_fn: Callable[[T], str],
    *,
    filter_fn: Callable[[T], bool] = lambda _: True,
    limit: Optional[int] = None,
    max_wait_time: int = 300,
    min_wait_time: int = 1,
    **function_kwargs: Any,
) -> Generator[T, None, None]:
    """Helper function to generate streams.

    :param results_fn: A function to call repeatedly, which outputs a list of objects.
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
        # noinspection DuplicatedCode
        first_key = last_key
        results = results_fn(**function_kwargs)
        for r in filter(filter_fn, results):
            unique_key = unique_key_fn(r)
            if unique_key not in found_keys:
                last_key = unique_key
                yield r
                count += 1
                if limit is not None and count >= limit:
                    return
                found_keys.add(unique_key)

        if first_key == last_key:  # no new results
            wait_time = min(2 * wait_time, max_wait_time)
        else:
            wait_time = min_wait_time

        time.sleep(wait_time)


async def async_stream_generator(
    results_fn: Callable[[KwArg(Any)], Iterable[T]],
    unique_key_fn: Callable[[T], str],
    *,
    filter_fn: Callable[[T], bool] = lambda _: True,
    limit: Optional[int] = None,
    max_wait_time: int = 300,
    min_wait_time: int = 1,
    **function_kwargs: Any,
) -> AsyncGenerator[T, None]:
    """Helper function to generate streams.

    :param results_fn: A function to call repeatedly, which outputs a list of objects.
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
        # noinspection DuplicatedCode
        first_key = last_key
        results = results_fn(**function_kwargs)
        for r in filter(filter_fn, results):
            unique_key = unique_key_fn(r)
            if unique_key not in found_keys:
                last_key = unique_key
                yield r
                count += 1
                if limit is not None and count >= limit:
                    return
                found_keys.add(unique_key)

        if first_key == last_key:  # no new results
            wait_time = min(2 * wait_time, max_wait_time)
        else:
            wait_time = min_wait_time

        await asyncio.sleep(wait_time)


async def _merge_streams(
    results_fns: Sequence[Callable[[KwArg(Any)], Iterable[T]]],
    unique_key_fns: Sequence[Callable[[T], str]],
    callback: Callable[[T], Any],
    *,
    filter_fn: Callable[[T], bool] = lambda _: True,
    limit: Optional[int] = None,
    max_wait_time: int = 300,
    min_wait_time: int = 1,
    **function_kwargs: Any,
):
    if limit is not None and limit <= 0:
        return None
    streams = [
        async_stream_generator(
            gen,
            uniq,
            filter_fn=filter_fn,
            limit=limit,
            max_wait_time=max_wait_time,
            min_wait_time=min_wait_time,
            **function_kwargs,
        )
        for gen, uniq in zip(results_fns, unique_key_fns)
    ]

    merged_streams = stream.merge(*streams)
    count = 0
    async with merged_streams.stream() as streamer:
        async for item in streamer:
            callback(item)
            count += 1
            if limit is not None and count >= limit:
                return


def stream_apply(
    results_fns: Sequence[Callable[[KwArg(Any)], Iterable[T]]],
    unique_key_fns: Sequence[Callable[[T], str]],
    callback: Callable[[T], Any],
    *,
    filter_fn: Callable[[T], bool] = lambda _: True,
    limit: Optional[int] = None,
    max_wait_time: int = 300,
    min_wait_time: int = 1,
    **function_kwargs: Any,
):
    """Helper function to generate streams.

    :param results_fns: A list of functions to call repeatedly, each of them
    outputting a list of objects.
    :param unique_key_fns: A list of functions (same length as `function`), where
    each of them takes an object and outputs a unique id.
    This is used to keep track of what results were already yielded.
    :param callback: A function that is applied to each of the objects.
    :param filter_fn: Ignore objects which return `True` for this function.
    :param limit: Maximum number of objects to yield.
    :param max_wait_time: If a function returns no new results, the time between calls
    to it increases. This sets the maximum time (in seconds) to wait before calling it
    again.
    :param min_wait_time: Minimum time (in seconds) to wait before calling the function
    again.
    :param function_kwargs: Keyword parameters that are passed to the function.
    """
    if len(results_fns) != len(unique_key_fns):
        msg = (
            f"The lengths of `generator_fns` and `unique_key_fns` need to be the same. "
            f"Got {len(results_fns)} and {len(unique_key_fns)}."
        )
        raise ValueError(msg)
    asyncio.run(
        _merge_streams(
            results_fns,
            unique_key_fns,
            callback,
            filter_fn=filter_fn,
            limit=limit,
            max_wait_time=max_wait_time,
            min_wait_time=min_wait_time,
            **function_kwargs,
        )
    )
