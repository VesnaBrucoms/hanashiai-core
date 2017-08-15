FROM python:3.6

COPY ./ /tmp/hanashiai_core/
RUN pip3 install -r /tmp/hanashiai_core/requirements/base.txt
RUN pip3 install /tmp/hanashiai_core/.

RUN rm -rf /tmp/hanashiai_core

COPY ./misc/ /opt/tests/