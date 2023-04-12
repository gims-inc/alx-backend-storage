#!/usr/bin/env python3
"""Python script that provides some stats
about Nginx logs stored in MongoDB:
"""
import pymongo


def nginx_stats(collection, methods):
    """
    first line: x logs where x is the number of documents in this collection
    second line: Methods:
    5 lines with the number of documents with the
        method = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    one line with the number of documents with:
        method=GET
        path=/status

    collection: mongo db colection
    methods: List[str]
    """

    num_of_logs = nginx_collection.count_documents({})
    print(f'{num_of_logs} logs')

    print("Methods:")

    for method in methods:
        count = nginx_collection.count_documents({"method": method})
        print(f'\tmethod {method}: {count}')

    status_checks = nginx_collection.count_documents(
        {"method": "GET", "path": "/status"})
    print(f'{status_checks} status check')


if __name__ == "__main__":
    client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]

    nginx_stats(nginx_collection, methods)
