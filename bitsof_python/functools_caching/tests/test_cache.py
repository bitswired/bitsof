from ..cache import recur_fibo_cache, recur_fibo_lru_cache, recur_fibo_no_cache


def test_valid() -> None:
    no_cache = recur_fibo_no_cache(10)
    cache = recur_fibo_cache(10)
    lru_cache = recur_fibo_lru_cache(10)

    assert no_cache == cache == lru_cache == 55
