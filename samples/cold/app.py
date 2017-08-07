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

import os
import sys

from hotfn.http import request
from hotfn.http import response


def parse_request(data):
    sys.stderr.write(data)
    rq = request.RawRequest(data)
    try:
        (method, url, dict_params,
         headers, version, data) = rq.parse_raw_request()
        headers.update({
            "Content-Type": "text/plain; charset=utf-8",
            "Date": "Sun, 26 Mar 2017 19:26:09 GMT"
        })
        rs = response.RawResponse(
            version, 200, "OK",
            response_data=data)
        sys.stdout.write(rs.dump())
    except Exception as ex:
        sys.stderr.write(data)
        sys.stderr.write(str(ex))
        sys.stdout.write(response.RawResponse(
            (1, 1), 500, "Internal Server Error",
            http_headers={
                "Date": "Sun, 26 Mar 2017 19:26:09 GMT"
            }).dump())
    finally:
        exit(0)

if __name__ == "__main__":
    if not os.isatty(sys.stdin.fileno()):
        data = sys.stdin.read()
        parse_request(data)
