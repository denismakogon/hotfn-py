package main

import (
	"fmt"
	"net/http"
	"bytes"
	"net/url"
	"io/ioutil"
	"net/http/httputil"
	"strconv"
)

func createRequest() {
	data := "hello:hello"
	var buf bytes.Buffer

	req := http.Request{
		Method: http.MethodGet,
		URL: &url.URL{
			Scheme: "http",
			Host: "localhost:8080",
			Path: "/v1/apps",
			RawQuery: "something=something&etc=etc",
		},
		ProtoMajor: 1,
		ProtoMinor: 1,
		Header: http.Header{
			"Host": []string{"localhost:8080"},
			"User-Agent": []string{"curl/7.51.0"},
			"Content-Length": []string{strconv.Itoa(len(data))},
			"Content-Type": []string{"application/x-www-form-urlencoded"},
		},
		ContentLength: int64(len(data)),
		Host: "localhost:8080",
	}
	buf.Write([]byte(data))
	req.Body = ioutil.NopCloser(&buf)
	raw, err := httputil.DumpRequest(&req, true)
	if err != nil {
		fmt.Println(fmt.Sprintf("Error %v", err))
	}
	fmt.Println(string(raw))
}


func main() {
	createRequest()
}
