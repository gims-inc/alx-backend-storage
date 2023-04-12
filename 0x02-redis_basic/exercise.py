#!/usr/bin/env python3
"""
Writing strings to Redis
"""
import redis
import uuid
from typing import Union


class Cache:
    def __init__(self) -> None:
        """
        store an instance of the Redis client
        and flush the instance
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """method that takes a data argument and returns a string.
        The method should generate a random key (e.g. using uuid),
        store the input data in Redis using the random key and

        data: (Union)
        return:  key(str)

        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)

        return key
