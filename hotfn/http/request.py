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


class RawRequest(object):

    def __init__(self, raw_request):
        self.raw = raw_request

    def parse_raw_request(self):
        """Parses raw HTTP request that contains:
         - method
         - route + query
         - headers
         - protocol version
         Optionally:
         - data

         Raw HTTP request may have next look:

            GET /v1/apps?something=something&etc=etc HTTP/1.1
            Host: localhost:8080
            Content-Length: 5
            Content-Type: application/x-www-form-urlencoded
            User-Agent: curl/7.51.0

            hello

        Each new line define by set of special characters:

            \n
            \r

        and combination is:

            \r\n

        :return: tuple of HTTP method, HTTP URL, HTTP query parameters,
        HTTP headers, HTTP proto version, HTTP raw data
        :rtype: tuple
        """

        def get_parts_by_identifier(raw_req, condition):
            return [part for part in raw_req.split("\r\n") if condition(part)]

        def setup_headers(raw_headers):
            result = {}
            for h in raw_headers:
                hk, hv = h.split(":", maxsplit=1)
                result.update({hk: hv.lstrip()})
            return result

        rest_data = get_parts_by_identifier(
            self.raw,
            lambda x: x.find(":") < 0 and x != "" and "\n" not in x)

        headers = setup_headers(get_parts_by_identifier(
            self.raw, lambda y: y.find(":") > 0 and y != ""))

        data = ''
        dict_params = {}
        try:
            content_length = int(
                headers.get("Content-Length",
                            headers.get("Fn_header_content_length", 0)))
            if content_length > 0:
                # if data sent, it will be presented
                # at the end of the raw request
                raw_data = self.raw.rsplit("\r\n", maxsplit=1).pop()
                data = raw_data[:content_length]
                # it may appear that data contains `:` chars (JSON)
                # in this case data will be appended to headers,
                # that why it must be dropped off
                headers = setup_headers(get_parts_by_identifier(
                    self.raw[:-(len(data) + 2)],
                    lambda y: y.find(":") > 0 and y != ""))

            method, route_query, version = rest_data.pop().split(" ")
            major_minor = version.replace("HTTP/", "").split(".")
            if len(major_minor) > 1:
                major, minor = major_minor
            else:
                major, minor = major_minor.pop(), "0"
            splitted_route_query = route_query.split("?")
            if len(splitted_route_query) == 2:
                url, params = splitted_route_query
                for pair in params.split("&"):
                    k, v = pair.split("=")
                    dict_params.update({k: v})
            else:
                url = splitted_route_query.pop()

            return method, url, dict_params, headers, (major, minor), data

        except (Exception, IndexError) as ex:
            raise Exception("Malformed HTTP method, route, version: {}. "
                            "Original error: {}".format(rest_data, str(ex)))
