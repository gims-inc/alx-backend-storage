#!/usr/bin/env python3
"""Python function that inserts a new
document in a collection based on kwargs
"""
import pymongo


def insert_school(mongo_collection, **kwargs):
    """perform an insert in nosqldb

    returns: _id
    """
    res = mongo_collection.insert_one(kwargs)
    return res.inserted_id
