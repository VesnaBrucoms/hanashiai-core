FROM alpine:3.6

RUN apk add --update python3

COPY ./ /tmp/hanashiai_core/
RUN pip3 install -r /tmp/hanashiai_core/requirements/base.txt
RUN python3 /tmp/hanashiai_core/setup.py install

RUN rm -rf /tmp/hanashiai_core