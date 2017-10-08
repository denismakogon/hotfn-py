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

import sys
import ujson

from hotfn import headers as http_headers


class RawResponse(object):

    def __init__(self, data, headers=None, status_code=200):
        self.status_code = status_code
        self.body = data
        if headers:
            if not isinstance(headers, http_headers.GoLikeHeaders):
                raise TypeError("headers should be of "
                                "`hotfn.headers.GoLikeHeaders` type!")
            self.headers = headers
        else:
            self.headers = http_headers.GoLikeHeaders({})

    def dump(self, stream, flush=True):
        raw_body = ujson.dumps(self.body)
        self.headers.set("content-length", len(raw_body))
        resp = ujson.dumps({
            "body": raw_body,
            "status_code": self.status_code,
            "headers": self.headers.for_dump()
        })
        print("Prepared response: {}".format(resp),
              file=sys.stderr, flush=True)
        result = stream.write(resp)
        if flush:
            stream.flush()
        return result
