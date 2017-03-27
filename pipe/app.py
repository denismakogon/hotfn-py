import os
import sys

from hotfn.http import response


if __name__ == "__main__":
    if not os.isatty(sys.stdin.fileno()):
        try:
            rs = response.RawResponse(
                (1, 1), 200, "OK",
                response_data="Ok, fine",
                http_headers={
                    "Date": "Sun, 26 Mar 2017 19:26:09 GMT",
                    "Content-Type": "text/plain; charset=utf-8",
                })
            print(rs.dump())
        except Exception:
            print(response.RawResponse(
                (1, 1), 500, "Internal Server Error",
                http_headers={
                    "Date": "Sun, 26 Mar 2017 19:26:09 GMT"
                }).dump())
