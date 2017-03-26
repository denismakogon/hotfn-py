import os
import sys

from hotfn.http import request
from hotfn.http import response


if __name__ == "__main__":
    while True:
        if not os.isatty(sys.stdin.fileno()):
            rq = request.RawRequest(sys.stdin.read())
            try:
                (method, url, dict_params,
                 headers, version, data) = rq.parse_raw_request()
                headers.update({
                    "Content-Type": "text/plain; charset=utf-8",
                    "Date": "Sun, 26 Mar 2017 19:26:09 GMT"
                })
                rs = response.RawResponse(
                    version, 200, "OK",
                    response_data=data,
                    http_headers=headers)
                print(rs.dump())
            except Exception as _:
                print(response.RawResponse(
                    (1, 1), 500, "Internal Server Error",
                    http_headers={
                        "Date": "Sun, 26 Mar 2017 19:26:09 GMT"
                    }).dump())
