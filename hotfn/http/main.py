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

import json
import os
import sys
import traceback

import hotfn.http.request
import hotfn.http.response


def main(app):
    if not os.isatty(sys.stdin.fileno()):
        with open("/dev/stdin", 'rb') as stdin:
            rq = hotfn.http.request.RawRequest(stdin)
            while True:
                try:
                    (method, url, dict_params,
                     headers, version, data) = rq.parse_raw_request()
                    rs = normal_dispatch(app,
                                         method=method,
                                         url=url,
                                         dict_params=dict_params,
                                         headers=headers,
                                         version=version,
                                         data=data)
                    print(rs.dump(), file=sys.stdout, flush=True)
                except (Exception, EOFError) as ex:
                    traceback.print_exc(file=sys.stderr)
                    print((hotfn.http.response.RawResponse(
                        (1, 1), 500, "Internal Server Error",
                        {}, str(ex)).dump()), file=sys.stdout)


class DispatchException(Exception):
    def __init__(self, status, message):
        self.status = status
        self.message = message

    def response(self):
        return hotfn.http.response.RawResponse(
            (1, 1), self.status, 'ERROR', {}, self.message)


def normal_dispatch(app, method=None, url=None,
                    dict_params=None, headers=None,
                    version=None, data=None):
    try:
        rs = app(method=method,
                 url=url,
                 dict_params=dict_params,
                 headers=headers,
                 version=version,
                 data=data)
        if isinstance(rs, hotfn.http.response.RawResponse):
            return rs
        elif isinstance(rs, str):
            return hotfn.http.response.RawResponse((1, 1), 200, 'OK', {}, rs)
        else:
            return hotfn.http.response.RawResponse(
                (1, 1), 200, 'OK',
                {'content-type': 'application/json'}, json.dumps(rs))
    except DispatchException as e:
        return e.response()
    except Exception as e:
        return hotfn.http.response.RawResponse(
            (1, 1), 500, 'ERROR', {}, str(e))


# TODO(denismakogon): this really should be content-type based decorator
# TODO(denismakogon): mode content types to add
def coerce_input_to_content_type(f):
    def app(method=None, url=None, dict_params=None,
            headers=None, version=None, data=None):
        content_type = headers.get("Content-Type")
        try:
            j = None
            if content_type == "application/json":
                j = json.load(data)
            if content_type in [
                    "application/text",
                    "application/x-www-form-urlencoded"]:
                j = data.readall().decode()
            if j is None:
                j = data.readall().decode()
        except Exception as ex:
            raise DispatchException(
                500, "Unexpected error: {}".format(str(ex)))
        return f(j)
    return app
