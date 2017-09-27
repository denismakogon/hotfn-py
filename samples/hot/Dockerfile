FROM python:3.6

ENV PYTHONUNBUFFERED 1

# (Sigh)
ARG DEVPI=docker.for.mac.localhost

RUN mkdir /code
WORKDIR /code
ADD . /code/
RUN pip install \
    $(if [ -n "$DEVPI" ]; then \
      echo "-i http://$DEVPI:3141/testuser/dev/+simple/ --trusted-host $DEVPI" ; \
      fi) \
    -r requirements.txt

ENTRYPOINT ["python3", "app.py"]
