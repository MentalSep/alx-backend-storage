#!/usr/bin/env python3


def update_topics(mongo_collection, name, topics):
    """Updates the topics of a school document based on the name"""
    filter = {"name": name}
    update = {"$set": {"topics": topics}}
    mongo_collection.update_one(filter, update)
