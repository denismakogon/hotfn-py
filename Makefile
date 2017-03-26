# Just builds
.PHONY: test-pipe

test-pipe:
	pip install -e . && go run pipe/main.go | python3 pipe/app.py

all: test-pipe
