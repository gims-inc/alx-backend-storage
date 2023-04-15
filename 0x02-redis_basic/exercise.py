#!/usr/bin/env python3
"""
Writing strings to Redis
Reading from Redis and recovering original type
"""
import redis
import uuid
from typing import Union, Optional, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Counts the number of times a function is called

    method: function to be decorated
    Returns: decorated function
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function for the decorated function

        *args: arguments passed
        **kwargs: keyword arguments passed
        Returns: return value of the decorated function
        """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """Counts the number of times a function is called
    
    method: function to be decorated
    Returns: decorated function
    """
    key = method.__qualname__
    inputs = key + ":inputs"
    outputs = key + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function for the decorated function
        
        *args: The arguments passed to the function
        **kwargs: The keyword arguments passed to the function
        Returns: return value of the decorated function
        """
        self._redis.rpush(inputs, str(args))
        data = method(self, *args, **kwargs)
        self._redis.rpush(outputs, str(data))
        return data

    return wrapper


def replay(method: Callable) -> None:
    """
    Replays the history of a function
    Args:
        method: The function to be decorated
    Returns:
        None
    """
    name = method.__qualname__
    cache = redis.Redis()
    calls = cache.get(name).decode("utf-8")
    print("{} was called {} times:".format(name, calls))
    inputs = cache.lrange(name + ":inputs", 0, -1)
    outputs = cache.lrange(name + ":outputs", 0, -1)
    for i, o in zip(inputs, outputs):
        print("{}(*{}) -> {}".format(name, i.decode('utf-8'),
                                     o.decode('utf-8')))


class Cache:
    def __init__(self) -> None:
        """
        store an instance of the Redis client
        and flush the instance
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
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
