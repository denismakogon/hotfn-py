FROM jjanzic/docker-python3-opencv

# (Sigh)
ARG DEVPI=docker.for.mac.localhost

RUN mkdir /code
ADD . /code/
RUN pip install \
    $(if [ -n "$DEVPI" ]; then \
      echo "-i http://$DEVPI:3141/testuser/dev/+simple/ --trusted-host $DEVPI" ; \
      fi) \
    -r requirements.txt

WORKDIR /code/
ENTRYPOINT ["python3", "app.py"]
