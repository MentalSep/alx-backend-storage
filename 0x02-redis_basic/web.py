#!/usr/bin/env python3
"""Module to store data in Redis."""
import requests
import redis
from functools import wraps
from typing import Callable


def cache_and_track_access(func: Callable) -> Callable:
    """Decorator to cache the result of the request and track access"""
    @wraps(func)
    def wrapper(url: str) -> str:
        r = redis.Redis()
        r.incr("count:{}".format(url))
        cached_page = r.get("{}".format(url))
        if cached_page:
            return cached_page.decode("utf-8")
        response = func(url)
        r.set("{}".format(url), response, 10)
        return response

    return wrapper


@cache_and_track_access
def get_page(url: str) -> str:
    """Fetch the page content"""
    return requests.get(url).text
