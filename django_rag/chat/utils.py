from typing import AsyncIterator, Tuple, Any


async def aenumerate(
    iterable: AsyncIterator[Any], start=0
) -> AsyncIterator[Tuple[str, Any]]:
    """Async version of enumerate function."""

    i = start
    async for x in iterable:
        yield i, x
        i += 1
