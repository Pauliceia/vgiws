#!/usr/bin/env python
# -*- coding: utf-8 -*-


from unittest import TestCase
from util.tester import UtilTester


# https://realpython.com/blog/python/testing-third-party-apis-with-mocks/


class TestAPIProject(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    def test_get_api_project_return_all_projects(self):
        expected = {
            'features': [
                {
                    'properties': {'removed_at': None, 'create_at': '2017-11-20 00:00:00', 'fk_user_id_owner': 1001, 'id': 1001},
                    'tags': [{'k': 'name', 'v': 'default'}, {'k': 'description', 'v': 'default project'}],
                    'type': 'Project'
                },
                {
                    'properties': {'removed_at': None, 'create_at': '2017-10-12 00:00:00', 'fk_user_id_owner': 1002, 'id': 1002},
                    'tags': [{'k': 'name', 'v': 'test_project'}, {'k': 'description', 'v': 'test_project'}],
                    'type': 'Project'
                },
                {
                    'properties': {'removed_at': None, 'create_at': '2017-12-23 00:00:00', 'fk_user_id_owner': 1002, 'id': 1003},
                    'tags': [{'k': 'name', 'v': 'project 3'}, {'k': 'description', 'v': 'test_project'}],
                    'type': 'Project'
                },
                {
                    'properties': {'removed_at': None, 'create_at': '2017-09-11 00:00:00', 'fk_user_id_owner': 1003, 'id': 1004},
                    'tags': [{'k': 'name', 'v': 'project 4'}, {'k': 'description', 'v': 'test_project'}],
                    'type': 'Project'
                },
                {
                    'properties': {'removed_at': None, 'create_at': '2017-06-04 00:00:00', 'fk_user_id_owner': 1003, 'id': 1005},
                    'tags': [{'k': 'name', 'v': 'project 5'}, {'k': 'description', 'v': 'test_project'}],
                    'type': 'Project'
                }
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_project(expected, project_id="")

    def test_get_api_project_return_project_by_project_id(self):
        expected = {
            'features': [
                {
                    'type': 'Project',
                    'tags': [{'k': 'name', 'v': 'default'},
                             {'k': 'description', 'v': 'default project'}],
                    'properties': {'removed_at': None, 'fk_user_id_owner': 1001,
                                   'id': 1001, 'create_at': '2017-11-20 00:00:00'}
                }
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_project(expected, project_id="1001")

    # def test_get_api_project_return_project_by_user_id(self):
    #     expected = {
    #         'features': [
    #             {
    #                 'type': 'Project',
    #                 'tags': [{'k': 'name', 'v': 'default'},
    #                          {'k': 'description', 'v': 'default project'}],
    #                 'properties': {'removed_at': None, 'fk_user_id_owner': 1001,
    #                                'id': 1001, 'create_at': '2017-10-20 00:00:00'}
    #             }
    #         ],
    #         'type': 'FeatureCollection'
    #     }
    #
    #     self.tester.api_project(expected, user_id="1001")

    def test_get_api_project_with_invalid_project_id(self):
        self.tester.api_project_invalid_parameter(project_id="abc")
        self.tester.api_project_invalid_parameter(project_id=0)
        self.tester.api_project_invalid_parameter(project_id=-1)
        self.tester.api_project_invalid_parameter(project_id="-1")
        self.tester.api_project_invalid_parameter(project_id="0")




# It is not necessary to pyt the main() of unittest here,
# because this file will be call by run_tests.py
