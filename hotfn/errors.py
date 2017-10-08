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

from hotfn import headers
from hotfn.http import response as http_response
from hotfn.json import response as json_response


# TODO(denismakogon): add HTTP version, headers, etc.
class HTTPDispatchException(Exception):

    def __init__(self, status, message):
        """

        :param status: HTTP status code
        :param message: error message
        """
        self.status = status
        self.message = message

    def response(self):
        return http_response.RawResponse(
            (1, 1), self.status, 'ERROR', {}, self.message)


class JSONDispatchException(Exception):

    def __init__(self, status, message):
        """

        :param status: HTTP status code
        :param message: error message
        """
        self.status = status
        self.message = message

    def response(self):
        resp_headers = headers.GoLikeHeaders({})
        resp_headers.set("content-type", "application/json; charset=utf-8")
        return json_response.RawResponse({
            "error": {
                "message": self.message,
            }
        }, headers=resp_headers, status_code=500)
