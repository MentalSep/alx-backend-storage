#!/usr/bin/env python3
"""Module to store data in Redis."""
import requests
import redis
from functools import wraps
from typing import Callable


def cache_and_track_access(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(url: str) -> str:
        """Cache the result of the request and track access"""
        r = redis.Redis()
        r.incr('count:{}'.format(url))
        result = r.get('result:{}'.format(url))
        if result:
            return result.decode('utf-8')
        result = func(url)
        r.set('count:{}'.format(url), 0)
        r.setex('result:{}'.format(url), 10, result)
        return result
    return wrapper


@cache_and_track_access
def get_page(url: str) -> str:
    """Fetch the page content"""
    return requests.get(url).text
