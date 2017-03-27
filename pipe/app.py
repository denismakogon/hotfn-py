import os
import sys
import json

from hotfn.http import response


if __name__ == "__main__":
    if not os.isatty(sys.stdin.fileno()):
        while True:
            try:
                rs = response.RawResponse(
                    (1, 1), 200, "OK",
                    http_headers={
                        "Date": "Sun, 26 Mar 2017 19:26:09 GMT",
                        "Content-Type": "text/plain; charset=utf-8",
                    },
                    response_data=json.dumps(dict(os.environ)),
                )
                print(rs.dump())
            except Exception:
                print(response.RawResponse(
                    (1, 1), 500, "Internal Server Error",
                    http_headers={
                        "Date": "Sun, 26 Mar 2017 19:26:09 GMT"
                    }).dump())
