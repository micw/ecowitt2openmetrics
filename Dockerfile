FROM alpine:3.18

RUN apk add --update --no-cache python3 py3-requests

ADD ecowitt2openmetrics.py /ecowitt2openmetrics.py

RUN ["/usr/bin/python3","/ecowitt2openmetrics.py"]
