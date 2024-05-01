#!/usr/bin/env python3
"""Module to store data in Redis."""
import uuid
import redis
from typing import Union, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """counts calls to a method and increments a Redis counter"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """stores the history of inputs and outputs for a particular function"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        input = str(args)
        self._redis.rpush(method.__qualname__ + ":inputs", input)
        output = method(self, *args, **kwargs)
        self._redis.rpush(method.__qualname__ + ":outputs", output)
        return output

    return wrapper


class Cache:
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Stores data in Redis and returns the generated key"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Callable = None) -> Union[str, bytes, int, float, None]:
        """applies an optional conversion function"""
        data = self._redis.get(key)
        if data is None:
            return None
        return fn(data) if fn else data

    def get_str(self, key: str) -> str:
        """Retrieves data from Redis and converts it to a string"""
        return self.get(key, lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """Retrieves data from Redis and converts it to an integer"""
        return self.get(key, int)
