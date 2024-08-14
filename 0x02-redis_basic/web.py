#!/usr/bin/env python3
import redis
import requests
from typing import Callable
from functools import wraps

redis_store = redis.Redis()
'''module level redid instance'''

def data_catcher(method: Callable) -> Callable:
    """caches output of stored data"""
    @wraps(method)
    def invoker(url: str) -> str:
        """wrapper func for caching output"""
        redis_store.incr(f'count:{url}')
        result = redis_store.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        result = method(url)
        redis_store.set(f'count:{url}', 0)
        redis_store.setex(f'result:{url}', 10, result)
        return result
    return invoker

@data_cacher
def get_page(url: str) -> str:
    """obtain html content of a url and returns it"""
    return requests.get(url).text
