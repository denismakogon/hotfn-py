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

import asyncio
import os
import sys

from hotfn.http import request
from hotfn.http import response


class FutureParser(object):

    def __init__(self):
        self.lines = []

    def add_line(self, *args):
        line = sys.stdin.readline()
        if line:
            self.lines.append(line)
            if "\r\n" not in line:
                self.parse_request()

    def parse_request(self):
        sys.stderr.write(str(self.lines))
        stdin = "".join(self.lines)
        sys.stderr.write("Income request %s".format(stdin))
        rq = request.RawRequest(stdin)
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
            sys.stderr.write(str(ex))
            sys.stdout.write(response.RawResponse(
                (1, 1), 500, "Internal Server Error",
                http_headers={
                    "Date": "Sun, 26 Mar 2017 19:26:09 GMT"
                }).dump())
        finally:
            self.lines = []


if __name__ == "__main__":
    if not os.isatty(sys.stdin.fileno()):
        loop = asyncio.get_event_loop()
        parse = FutureParser()

        task = loop.add_reader(sys.stdin.fileno(), parse.add_line, parse)
        loop.run_forever()
