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
    Set,
    TypeVar,
)

from aiostream import stream
from mypy_extensions import KwArg

T = TypeVar("T")


class StreamYielder:
    """Helper class to manage a stream and keep track of previously seen results."""

    def __init__(
        self,
        *,
        skip_existing: bool,
        filter_fn: Callable[[T], bool],
        unique_key_fn: Callable[[T], str],
        limit: Optional[int],
        min_wait_time: int,
        max_wait_time: int,
    ):
        """Initialize StreamYielder.

        :param unique_key_fn: A function that takes an object and outputs a unique id.
        This is used to keep track of what results were already yielded.
        :param filter_fn: Ignore objects which return `True` for this function.
        :param limit: Maximum number of objects to yield.
        :param max_wait_time: If a function returns no new results, the time between
        calls to it increases. This sets the maximum time (in seconds) to wait before
        calling it again.
        :param min_wait_time: Minimum time (in seconds) to wait before calling the
        function again.
        :param skip_existing: If `True`, skip existing results and return only future
        ones.
        In practice, this means the results from the first request are ignored.
        """
        self.skip_existing = skip_existing
        self.filter_fn = filter_fn
        self.unique_key_fn = unique_key_fn
        self.limit = limit

        self.results_count = 0
        self.requests_count = 0
        self.found_keys: Set[str] = set()
        self.last_seen_key = ""

        self.wait_time = min_wait_time
        self.min_wait_time = min_wait_time
        self.max_wait_time = max_wait_time

    def yield_results(self, results: Iterable[T]) -> Generator[Optional[T], None, None]:
        """Iterate through the results.

        :param results: Results from one to the generator function.
        """
        skipping_yield = False
        if self.requests_count == 1 and self.skip_existing:
            skipping_yield = True
        for r in filter(self.filter_fn, results):  # type: ignore[var-annotated, arg-type]
            unique_key = self.unique_key_fn(r)
            if unique_key not in self.found_keys:
                self.last_seen_key = unique_key
                if not skipping_yield:
                    yield r
                    self.results_count += 1
                if self.limit is not None and self.results_count >= self.limit:
                    yield None
                self.found_keys.add(unique_key)

    def get_wait_time(self, first_key: str) -> int:
        """Get how long we should wait.

        :param first_key: First key seen in the previous iteration.
        If this is the same as `self.last_seen_key` it means that no new content
        was seen in the last request, and so wait time should increase.
        """
        if first_key == self.last_seen_key:  # no new results
            self.wait_time = min(2 * self.wait_time, self.max_wait_time)
        else:
            self.wait_time = self.min_wait_time
        return self.wait_time


def stream_generator(
    results_fn: Callable[[KwArg(Any)], Iterable[T]],
    unique_key_fn: Callable[[T], str],
    *,
    filter_fn: Callable[[T], bool] = lambda _: True,
    limit: Optional[int] = None,
    max_wait_time: int = 300,
    min_wait_time: int = 1,
    skip_existing: bool = False,
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
    :param skip_existing: If `True`, skip existing results and return only future ones.
    In practice, this means the results from the first request are ignored.
    :param function_kwargs: Keyword parameters that are passed to the function.
    """
    stream_obj = StreamYielder(
        skip_existing=skip_existing,
        filter_fn=filter_fn,
        unique_key_fn=unique_key_fn,
        limit=limit,
        min_wait_time=min_wait_time,
        max_wait_time=max_wait_time,
    )
    while True:
        first_key = stream_obj.last_seen_key
        results = results_fn(**function_kwargs)
        for r in stream_obj.yield_results(results):
            if r is None:
                return
            yield r

        time.sleep(stream_obj.get_wait_time(first_key))


async def async_stream_generator(
    results_fn: Callable[[KwArg(Any)], Iterable[T]],
    unique_key_fn: Callable[[T], str],
    *,
    filter_fn: Callable[[T], bool] = lambda _: True,
    limit: Optional[int] = None,
    max_wait_time: int = 300,
    min_wait_time: int = 1,
    skip_existing: bool = False,
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
    :param skip_existing: If `True`, skip existing results and return only future ones.
    In practice, this means the results from the first request are ignored.
    :param function_kwargs: Keyword parameters that are passed to the function.
    """
    stream_obj = StreamYielder(
        skip_existing=skip_existing,
        filter_fn=filter_fn,
        unique_key_fn=unique_key_fn,
        limit=limit,
        min_wait_time=min_wait_time,
        max_wait_time=max_wait_time,
    )
    while True:
        first_key = stream_obj.last_seen_key
        results = results_fn(**function_kwargs)
        for r in stream_obj.yield_results(results):
            if r is None:
                return
            yield r

        await asyncio.sleep(stream_obj.get_wait_time(first_key))


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
