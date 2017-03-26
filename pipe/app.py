import sys

from hotfn.http import request
from hotfn.http import response


if __name__ == "__main__":
    # while True:
    rq = request.RawRequest(sys.stdin.read())
    method, url, dict_params, headers, version, data = rq.parse_raw_request()
    response = response.RawResponse(
        version, 200, "OK", response_data=data, http_headers=headers)
    print(response.dump())
