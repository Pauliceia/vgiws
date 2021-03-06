#!/usr/bin/env python
# -*- coding: utf-8 -*-


def get_subquery_user_layer_table(**kwargs):
    # DEFAULT WHERE
    # by default, get all results that are visible (that exist)
    # conditions_of_where = ["removed_at is NULL"]  # visible=True
    conditions_of_where = []  # visible=True

    # conditions of WHERE CLAUSE
    if "layer_id" in kwargs and kwargs["layer_id"] is not None:
        conditions_of_where.append("layer_id = {0}".format(kwargs["layer_id"]))

    if "user_id" in kwargs and kwargs["user_id"] is not None:
        conditions_of_where.append("user_id = '{0}'".format(kwargs["user_id"]))

    if "is_the_creator" in kwargs and kwargs["is_the_creator"] is not None:
        conditions_of_where.append("is_the_creator = {0}".format(kwargs["is_the_creator"]))

    # default get all features, without where clause
    where_clause = ""

    # if there is some conditions, put in where_clause
    if conditions_of_where:
        where_clause = "WHERE " + " AND ".join(conditions_of_where)

    # default get all features
    subquery_table = """
        (
            SELECT * FROM user_layer {0} ORDER BY layer_id, user_id
        ) AS user_layer
    """.format(where_clause)

    return subquery_table
