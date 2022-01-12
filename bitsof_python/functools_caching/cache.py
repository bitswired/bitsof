from functools import cache, lru_cache
from timeit import Timer
from typing import Any, Callable


def recur_fibo_no_cache(n: int) -> int:
    """Recursive fibo without cache"""
    if n <= 1:
        return n
    else:
        return recur_fibo_no_cache(n - 1) + recur_fibo_no_cache(n - 2)


@cache
def recur_fibo_cache(n: int) -> int:
    """Recursive fibo with cache (using functools cache decorator)"""
    if n <= 1:
        return n
    else:
        return recur_fibo_cache(n - 1) + recur_fibo_cache(n - 2)


@lru_cache(maxsize=5)
def recur_fibo_lru_cache(n: int) -> int:
    """Recursive fibo with lru cache (using functools lru_cache decorator)"""
    if n <= 1:
        return n
    else:
        return recur_fibo_lru_cache(n - 1) + recur_fibo_lru_cache(n - 2)


def exec_and_clear(f: Callable[[int], int], arg: Any) -> int:
    a = f(arg)
    f.cache_clear()  # type: ignore
    return a


def measure_plot(number: int, inputs: list[int]) -> tuple[list[float], list[float]]:
    no_cache_times = []
    for n in inputs:
        no_cache_timer = Timer(lambda: recur_fibo_no_cache(n))
        no_cache_time = no_cache_timer.timeit(number=number)
        no_cache_times.append(no_cache_time / number)

    cache_times = []
    recur_fibo_cache.cache_clear()
    for n in inputs:
        cache_timer = Timer(lambda: recur_fibo_cache(n))
        cache_time = cache_timer.timeit(number=number)
        cache_times.append(cache_time / number)

    return no_cache_times, cache_times


if __name__ == "__main__":
    N = 35
    TIMEIT_NUMBER = 10

    # Compute execution time for no-cache, cache and LRU cache
    no_cache_timer = Timer(lambda: recur_fibo_no_cache(N))
    no_cache_time = no_cache_timer.timeit(number=TIMEIT_NUMBER) / TIMEIT_NUMBER
    print(f"Execution time without cache: {no_cache_time:.2e}")

    cache_timer = Timer(lambda: exec_and_clear(recur_fibo_cache, N))
    cache_time = cache_timer.timeit(number=TIMEIT_NUMBER) / TIMEIT_NUMBER
    print(
        f"Execution time with cache: {cache_time:.2e}",
    )

    lru_cache_timer = Timer(lambda: exec_and_clear(recur_fibo_lru_cache, N))
    lru_cache_time = lru_cache_timer.timeit(number=TIMEIT_NUMBER) / TIMEIT_NUMBER
    print(
        f"Execution time with LRU cache: {lru_cache_time:.2e}",
    )

    print()

    # Compute speedup for cache and LRU cache over no-cache
    speedup = round(no_cache_time / cache_time)
    print(f"Speedup cache over no-cache: x{speedup:.2e}")

    speedup = round(no_cache_time / lru_cache_time)
    print(f"Speedup LRU cache over no-cache (max size 2): x{speedup:.2e}")

    print()

    inputs = list(range(0, N + 1, 1))
    no_cache_times, cache_times = measure_plot(TIMEIT_NUMBER, inputs)

    print(inputs)
    print(no_cache_times)
    print(cache_times)
