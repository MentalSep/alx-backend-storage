#!/usr/bin/env python3
"""Module to store data in Redis."""
import requests
import redis
from functools import wraps


def cache_and_track_access(func):
    @wraps(func)
    def wrapper(url):
        """Cache the result of the request and track access"""
        r = redis.Redis()

        r.incr("count:{}".format(url))

        cached_content = r.get(url)
        if cached_content:
            return cached_content.decode()

        response = func(url)
        content = response.text

        r.setex(url, 10, content)

        return content
    return wrapper


@cache_and_track_access
def get_page(url: str) -> str:
    """Fetch the page content"""
    return requests.get(url)
