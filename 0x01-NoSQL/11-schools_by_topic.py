#!/usr/bin/env python3
"""Module schools_by_topic"""


def schools_by_topic(mongo_collection, topic):
    """Return the list of schools having a specific topic"""
    return list(mongo_collection.find({"topics": topic}))
