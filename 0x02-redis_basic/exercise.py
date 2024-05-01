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


def call_history(fn: Callable) -> Callable:
    """stores the history of inputs and outputs for a particular function"""
    @wraps(fn)
    def wrapper(self, *args, **kwargs):
        input_key = "{}:inputs".format(fn.__qualname__)
        output_key = "{}:outputs".format(fn.__qualname__)

        self._redis.rpush(input_key, str(args))
        output = fn(self, *args, **kwargs)
        self._redis.rpush(output_key, output)
        return output

    return wrapper


def replay(method: Callable) -> None:
    """display the history of calls of a particular function"""
    r = redis.Redis()
    method_name = method.__qualname__
    inputs = r.lrange(method_name + ":inputs", 0, -1)
    outputs = r.lrange(method_name + ":outputs", 0, -1)

    print(method_name + " was called {} times:".format(len(inputs)))
    for i, o in zip(inputs, outputs):
        print(method_name + "(*{}) -> {}".format(
            i.decode("utf-8"), o.decode("utf-8")))


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
