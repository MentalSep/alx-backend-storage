#!/usr/bin/env python3
"""Module to store data in Redis."""
import uuid
import redis
from typing import Union


class Cache:
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Stores data in Redis and returns the generated key"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
