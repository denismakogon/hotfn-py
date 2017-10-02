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


class RawResponse(object):
    PATTERN = ("HTTP/{proto_major}.{proto_minor} "
               "{int_status} {verbose_status}\r\n"
               "{headers}")

    def __init__(self, http_proto_version, status_code, verbose_status,
                 http_headers=None, response_data=None):
        """Sets up raw response
        :param http_proto_version: HTTP protocol version
        :type http_proto_version: tuple
        :param status_code: HTTP response code
        :type status_code: int
        :param verbose_status: HTTP response status
        :type verbose_status: str
        :param http_headers: HTTP response headers
        :type http_headers: dict
        :param response_data: string representation of data
        :type response_data: str
        """

        http_headers = http_headers if http_headers else {}
        self.http_proto = http_proto_version
        self.int_status = status_code
        self.verbose_status = verbose_status
        self.response_data, content_len = self.__encode_data(response_data)
        if self.response_data:
            if not http_headers.get("Content-Type"):
                http_headers.update({
                    "Content-Type": "text/plain; charset=utf-8",
                })
            http_headers.update({
                "Content-Length": content_len,
            })
        self.headers = self.__encode_headers(http_headers)

    def __encode_headers(self, headers):
        if headers:
            result = ""
            for hk, hv in headers.items():
                result += "{}: {}\r\n".format(hk, hv)
            return result + "\r\n"
        return ""

    def __encode_data(self, data):
        if isinstance(data, bytes):
            return data, len(data)
        enc = str(data).encode('utf-8')
        return enc, len(enc)

    def dump(self, stream, flush=True):
        format_map = {
            "proto_major": self.http_proto[0],
            "proto_minor": self.http_proto[1],
            "int_status": self.int_status,
            "verbose_status": self.verbose_status,
            "headers": self.headers,
        }
        result = stream.write(
            self.PATTERN.format(**format_map).encode('utf-8') +
            self.response_data + "\n".encode("utf-8"))
        if flush:
            stream.flush()
        return result
