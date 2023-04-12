#!/usr/bin/env python3
"""
Writing strings to Redis
Reading from Redis and recovering original type 
"""
import redis
import uuid
from typing import Union, Optional, Callable


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

    def get(self, key: str, fn: Optional[Callable]
            = None) -> Union[str, bytes, int, float]:
        """Gets data from redis cache
        """
        data = self._redis.get(key)
        if data and fn and callable(fn):
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """Gets data as string from redis cache

        key: str
        return: str
        """
        data = self.get(key, lambda x: x.decode('utf-8'))
        return data

    def get_int(self, key: str) -> int:
        """Gets data as integer from redis cache

        key: str
        Returns: data(int)
        """
        data = self
