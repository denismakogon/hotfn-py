[![Build Status](https://travis-ci.org/denismakogon/hotfn-py.svg?branch=master)](https://travis-ci.org/denismakogon/hotfn-py)

HTTP over STDIN/STDOUT lib parser
=================================

Purpose of this library to provide simple interface to parse HTTP 1.1 requests represented as string

Raw HTTP request
----------------

Parses raw HTTP request that contains:
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

This type of class stands for HTTP request parsing to a sane structure of:

 - HTTP request method
 - HTTP request URL
 - HTTP request query string represented as map
 - HTTP request headers represented as map
 - HTTP protocol version represented as tuple of major and minor versions
 - HTTP request body

```python
import sys
from hotfn.http import request

req = request.RawRequest(sys.stdin.read())
method, url, query_parameters, headers, (major, minor), body = req.parse_raw_request()
```

Raw HTTP response
-----------------

This type of class stands for transforming HTTP request object into valid string representation

```python
import sys
from hotfn.http import request
from hotfn.http import response

req = request.RawRequest(sys.stdin.read())
method, url, query_parameters, headers, (major, minor), body = req.parse_raw_request()
resp = response.RawResponse((major, minor), 200, "OK", response_data=body)
print(resp.dump())
```

Example
-------

Assume we have HTTP 1.1 request:
```bash
GET /v1/apps?something=something&etc=etc HTTP/1.1
Host: localhost:8080
Content-Length: 11
Content-Type: application/x-www-form-urlencoded
User-Agent: curl/7.51.0

hello:hello

```
This request can be transformed into data structure described above.
Using code snippet mentioned above request data can be used to assemble a response object of the following view:
```bash
HTTP/1.1 200 OK
Content-Length: 11
Content-Type: text/plain; charset=utf-8

hello:hello

```
This is totally valid HTTP response object.

Notes
-----

Please be aware that response object by default sets content type as `text/plain; charset=utf-8`. If you need to change it use following code:
```python
import sys
from hotfn.http import request
from hotfn.http import response

req = request.RawRequest(sys.stdin.read())
method, url, query_parameters, headers, (major, minor), body = req.parse_raw_request()
resp = response.RawResponse((major, minor), 200, "OK", response_data=body)
resp.headers["Content-Type"] = "application/json"
print(resp.dump())

```
