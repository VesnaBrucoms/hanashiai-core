FROM python:3.6

COPY ./ /tmp/hanashiai_core/
RUN pip3 install /tmp/hanashiai_core/.

RUN rm -rf /tmp/hanashiai_core

ENV CLIENT_ID id
ENV CLIENT_SECRET secret