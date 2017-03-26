# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import testtools

from hotfn.http import request
from hotfn.tests import data


class TestRequestParser(testtools.TestCase):

    def setUp(self):
        super(TestRequestParser, self).setUp()

    def tearDown(self):
        super(TestRequestParser, self).tearDown()

    def test_parse_no_data(self):
        req_parser = request.RawRequest(data.request_no_data)
        (method, url, params, headers,
         proto_version, request_data) = req_parser.parse_raw_request()
        self.assertEqual("GET", method)
        self.assertIn("Host", headers)
        self.assertIn("Accept", headers)
        self.assertIn("User-Agent", headers)
        self.assertEqual(("1", "1"), proto_version)
        self.assertEqual('', request_data)
        self.assertIn("something", params)

    def test_parse_no_query(self):
        req_parser = request.RawRequest(data.request_no_query)
        (method, url, params, headers,
         proto_version, request_data) = req_parser.parse_raw_request()
        self.assertEqual("GET", method)
        self.assertIn("Host", headers)
        self.assertIn("Accept", headers)
        self.assertIn("User-Agent", headers)
        self.assertEqual(("1", "1"), proto_version)
        self.assertEqual('', request_data)
        self.assertEqual({}, params)

    def test_parse_data(self):
        req_parser = request.RawRequest(data.request_with_query_and_data)
        (method, url, params, headers,
         proto_version, request_data) = req_parser.parse_raw_request()
        self.assertEqual("GET", method)
        self.assertIn("Host", headers)
        self.assertIn("Content-Type", headers)
        self.assertIn("Content-Length", headers)
        self.assertEqual("11", headers.get("Content-Length"))
        self.assertIn("User-Agent", headers)
        self.assertEqual(("1", "1"), proto_version)
        self.assertEqual("hello:hello", request_data)
        self.assertIn("something", params)
