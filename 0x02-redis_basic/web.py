#!/usr/bin/env python3
"""Module to store data in Redis."""
import requests
import redis
from functools import wraps


def cache_and_track_access(func):
    @wraps(func)
    def wrapper(url):
        """Cache the result of the request and track access"""
        key = "cached:{}".format(url)
        r = redis.Redis()
        r.incr("count:{}".format(url))
        if r.get(key):
            return r.get(key).decode('utf-8')

        result = func(url)
        r.set(key, result)
        return result

    return wrapper


@cache_and_track_access
def get_page(url: str) -> str:
    """Fetch the page content"""
    return requests.get(url).text
