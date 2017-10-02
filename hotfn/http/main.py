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

import functools
import io
import json
import os
import sys

import traceback


from hotfn.http import errors
from hotfn.http import request
from hotfn.http import response


def main(app):
    """
    Request handler app dispatcher entry point
    :param app: request handler app
    :type app: types.Callable
    :return: None
    """
    if not os.isatty(sys.stdin.fileno()):
        with os.fdopen(sys.stdin.fileno(), 'rb') as stdin:
            with os.fdopen(sys.stdout.fileno(), 'wb') as stdout:
                rq = request.RawRequest(stdin)
                while True:
                    try:
                        context, data = rq.parse_raw_request()
                        rs = normal_dispatch(app, context, data=data)
                        rs.dump(stdout)
                    except EOFError:
                        # The Fn platform has closed stdin; there's no way to
                        # get additional work.
                        return
                    except errors.DispatchException as ex:
                        # If the user's raised an error containing an explicit
                        # response, use that
                        ex.response().dump(stdout)
                    except Exception as ex:
                        traceback.print_exc(file=sys.stderr)
                        response.RawResponse(
                            (1, 1), 500, "Internal Server Error",
                            {}, str(ex)).dump(stdout)


def normal_dispatch(app, context, data=None):
    """
    Request handler app dispatcher
    :param app: request handler app
    :type app: types.Callable
    :param context: request context
    :type context: request.RequestContext
    :param data: request body
    :type data: io.BufferedIOBase
    :return: raw response
    :rtype: response.RawResponse
    """
    try:
        rs = app(context, data=data)
        if isinstance(rs, response.RawResponse):
            return rs
        elif isinstance(rs, str):
            return response.RawResponse(context.version, 200, 'OK', {}, rs)
        elif isinstance(rs, bytes):
            return response.RawResponse(
                context.version, 200, 'OK',
                {'content-type': 'application/octet-stream'},
                rs.decode("utf8"))
        else:
            return response.RawResponse(
                context.version, 200, 'OK',
                {'content-type': 'application/json'}, json.dumps(rs))
    except errors.DispatchException as e:
        return e.response()
    except Exception as e:
        return response.RawResponse(
            context.version, 500, 'ERROR', {}, str(e))


def coerce_input_to_content_type(f):

    @functools.wraps(f)
    def app(context, data=None):
        """
        Request handler app dispatcher decorator
        :param context: request context
        :type context: request.RequestContext
        :param data: request body
        :type data: io.BufferedIOBase
        :return: raw response
        :rtype: response.RawResponse
        :return:
        """
        # TODO(jang): The content-type header has some internal structure;
        # actually provide some parsing for that
        content_type = context.headers.get("content-type")
        try:
            request_body = io.TextIOWrapper(data)
            # TODO(denismakogon): XML type to add
            if content_type == "application/json":
                body = json.load(request_body)
            elif content_type in ["text/plain"]:
                body = request_body.read()
            else:
                body = request_body.read()
        except Exception as ex:
            raise errors.DispatchException(
                500, "Unexpected error: {}".format(str(ex)))

        # this is user's request handler
        return f(context, body)

    return app
