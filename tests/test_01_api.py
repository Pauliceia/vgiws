#!/usr/bin/env python
# -*- coding: utf-8 -*-


from unittest import TestCase
from json import loads, dumps
from requests import get

from util.tester import UtilTester


# TODO: create cases of test:
# TODO: DELETE A ELEMENT WITH ID THAT DOESN'T EXIST


class TestAPI(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    def test_get_api_create_changeset_without_login(self):
        # do a GET call
        response = get('http://localhost:8888/api/changeset/create/')

        self.assertEqual(response.status_code, 403)

        expected = {'status': 403, 'statusText': 'It needs a user looged to access this URL'}
        resulted = loads(response.text)  # convert string to dict/JSON

        self.assertEqual(expected, resulted)

    def test_get_api_crud_elements_with_login(self):
        # DO LOGIN
        self.tester.do_login()

        # CREATE A CHANGESET
        changeset = self.tester.create_a_changeset()

        # get the id of changeset to use in ADD element and CLOSE changeset
        fk_id_changeset = changeset["plc"]["changeset"]["properties"]["id"]

        # ADD ELEMENTS
        node = {
            'type': 'FeatureCollection',
            'crs': {"properties": {"name": "EPSG:4326"}, "type": "name"},
            'features': [
                {
                    'tags': [{'k': 'event', 'v': 'robbery'},
                             {'k': 'date', 'v': '1910'}],
                    'type': 'Feature',
                    'properties': {'id': -1, 'fk_changeset_id': fk_id_changeset},
                    'geometry': {
                        'type': 'MultiPoint',
                        'coordinates': [[-23.546421, -46.635722]]
                    },
                }
            ]
        }
        node = self.tester.add_a_element(node)  # return the same element with the id generated

        way = {
            'type': 'FeatureCollection',
            'crs': {"properties": {"name": "EPSG:4326"}, "type": "name"},
            'features': [
                {
                    'tags': [{'k': 'highway', 'v': 'residential'},
                             {'k': 'start_date', 'v': '1910-12-08'},
                             {'k': 'end_date', 'v': '1930-03-25'}],
                    'type': 'Feature',
                    'properties': {'id': -1, 'fk_changeset_id': fk_id_changeset},
                    'geometry': {
                        'type': 'MultiLineString',
                        'coordinates': [[[-54, 33], [-32, 31], [-36, 89]]]
                    },
                }
            ]
        }
        way = self.tester.add_a_element(way)

        area = {
            'type': 'FeatureCollection',
            'crs': {"properties": {"name": "EPSG:4326"}, "type": "name"},
            'features': [
                {
                    'tags': [{'k': 'building', 'v': 'cathedral'},
                             {'k': 'start_date', 'v': '1900-11-12'},
                             {'k': 'end_date', 'v': '1915-12-25'}],
                    'type': 'Feature',
                    'properties': {'id': -1, 'fk_changeset_id': fk_id_changeset},
                    'geometry': {
                        'type': 'MultiPolygon',
                        'coordinates': [[[[-12, 32], [-23, 74], [-12, 32]]]]
                    },
                }
            ]
        }
        area = self.tester.add_a_element(area)

        # VERIFY IN DB, IF THE ELEMENTS EXIST
        self.tester.verify_if_element_was_add_in_db(node)
        self.tester.verify_if_element_was_add_in_db(way)
        self.tester.verify_if_element_was_add_in_db(area)

        # REMOVE THE ELEMENTS CREATED
        self.tester.delete_element(node)
        self.tester.delete_element(way)
        self.tester.delete_element(area)

        # CLOSE THE CHANGESET
        self.tester.close_a_changeset(fk_id_changeset)

        # DO LOGOUT
        self.tester.do_logout()

        ################################################################################
        # TRY TO CREATE ANOTHER CHANGESET WITHOUT LOGIN
        ################################################################################

        # do a GET call, sending a changeset to add in DB
        response = self.tester.session.get('http://localhost:8888/api/changeset/create/',
                                           data=dumps(changeset), headers=self.tester.headers)

        # it is not possible to create a changeset without login, so get a 403 Forbidden
        self.assertEqual(response.status_code, 403)

    def test_get_api_crud_elements_that_not_exist_with_login(self):
        # DO LOGIN
        self.tester.do_login()

        # CREATE A CHANGESET
        changeset = self.tester.create_a_changeset()

        # get the id of changeset to use in ADD element and CLOSE changeset
        fk_id_changeset = changeset["plc"]["changeset"]["properties"]["id"]

        # ADD ELEMENTS
        node = {
            'type': 'FeatureCollection',
            'crs': {"properties": {"name": "EPSG:4326"}, "type": "name"},
            'features': [
                {
                    'tags': [{'k': 'event', 'v': 'robbery'},
                             {'k': 'date', 'v': '1910'}],
                    'type': 'Feature',
                    'properties': {'id': -1, 'fk_changeset_id': fk_id_changeset},
                    'geometry': {
                        'type': 'MultiPoint',
                        'coordinates': [[-23.546421, -46.635722]]
                    },
                }
            ]
        }

        way = {
            'type': 'FeatureCollection',
            'crs': {"properties": {"name": "EPSG:4326"}, "type": "name"},
            'features': [
                {
                    'tags': [{'k': 'highway', 'v': 'residential'},
                             {'k': 'start_date', 'v': '1910-12-08'},
                             {'k': 'end_date', 'v': '1930-03-25'}],
                    'type': 'Feature',
                    'properties': {'id': -2, 'fk_changeset_id': fk_id_changeset},
                    'geometry': {
                        'type': 'MultiLineString',
                        'coordinates': [[[-54, 33], [-32, 31], [-36, 89]]]
                    },
                }
            ]
        }

        area = {
            'type': 'FeatureCollection',
            'crs': {"properties": {"name": "EPSG:4326"}, "type": "name"},
            'features': [
                {
                    'tags': [{'k': 'building', 'v': 'cathedral'},
                             {'k': 'start_date', 'v': '1900-11-12'},
                             {'k': 'end_date', 'v': '1915-12-25'}],
                    'type': 'Feature',
                    'properties': {'id': -3, 'fk_changeset_id': fk_id_changeset},
                    'geometry': {
                        'type': 'MultiPolygon',
                        'coordinates': [[[[-12, 32], [-23, 74], [-12, 32]]]]
                    },
                }
            ]
        }

        # VERIFY IN DB, IF THE ELEMENTS EXIST
        self.tester.verify_if_element_was_not_add_in_db(node)
        self.tester.verify_if_element_was_not_add_in_db(way)
        self.tester.verify_if_element_was_not_add_in_db(area)

        # REMOVE THE ELEMENTS CREATED
        # self.tester.delete_element(node)
        # self.tester.delete_element(way)
        # self.tester.delete_element(area)

        # CLOSE THE CHANGESET
        self.tester.close_a_changeset(fk_id_changeset)

        # DO LOGOUT
        self.tester.do_logout()




# TODO: create a test to remove the elements added


# It is not necessary to pyt the main() of unittest here,
# because this file will be call by run_tests.py
