#!/usr/bin/env python3
"""Module for top_students"""

def top_students(mongo_collection):
    """Returns all students sorted by average score in descending order"""

    pipeline = [
        {"$unwind": "$topics"},
        {"$group": {
                "_id": "$_id",
                "name": {"$first": "$name"},
                "topics": {"$push": "$topics"},
                "averageScore": {"$avg": "$topics.score"}
            }},
        {"$sort": {"averageScore": -1}}
        ]

    cursor = mongo_collection.aggregate(pipeline)
    return list(cursor)
