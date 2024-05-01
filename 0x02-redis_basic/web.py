#!/usr/bin/env python3
"""Module to store data in Redis."""
from functools import wraps
from typing import Callable
import requests
import redis


def cache_and_track_access(fn: Callable) -> Callable:
    """Decorator for get_page"""
    @wraps(fn)
    def wrapper(url: str) -> str:
        """ Wrapper function"""
        r = redis.Redis()
        r.incr(f"count:{url}")
        cached_page = r.get(f"{url}")
        if cached_page:
            return cached_page.decode("utf-8")
        response = fn(url)
        r.set(f"{url}", response, 10)
        return response

    return wrapper


@cache_and_track_access
def get_page(url: str) -> str:
    """ Get the content of a web page."""
    return requests.get(url).text
