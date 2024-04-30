#!/usr/bin/env python3
"""Module for printing statistics about Nginx logs"""
from pymongo import MongoClient


def main():
    """retrieves and prints statistics about Nginx logs"""
    client = MongoClient()  # default host and port (i.e. localhost:27017)
    collection = client.logs.nginx

    total_logs = collection.count_documents({})
    status_checks = collection.count_documents({"path": "/status"})
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_counts = {}
    for method in methods:
        count = collection.count_documents({"method": method})
        method_counts[method] = count

    print("{} logs".format(total_logs))
    print("Methods:")
    for method, count in method_counts.items():
        print("\tmethod {}: {}".format(method, count))
    print("{} status check".format(status_checks))


if __name__ == "__main__":
    main()
