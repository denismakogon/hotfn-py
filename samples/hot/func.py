import asyncio
import sys

from hotfn.http import request
from hotfn.http import response


class MyProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        print('pipe opened', file=sys.stderr, flush=True)

    def data_received(self, data):
        data = data.decode()
        req = request.RawRequest(data)
        (method, url, dict_params,
         headers, http_version, req_data) = req.parse_raw_request()

        rs = response.RawResponse(
            http_version, 200, "OK",
            response_data=data)
        print(rs.dump(), file=sys.stdout, flush=True)

        print('received: {!r}'.format(data), file=sys.stderr, flush=True)

    def connection_lost(self, exc):
        print('pipe closed', file=sys.stdout, flush=True)


if __name__ == "__main__":
    loop = asyncio.SelectorEventLoop()
    loop.run_until_complete(
        loop.connect_read_pipe(
            MyProtocol, open("/dev/stdin", "rb", buffering=0)))
    loop.run_forever()
    loop.close()
