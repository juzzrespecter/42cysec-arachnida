FROM alpine:latest

RUN apk add python3 py3-pip \
    && apk cache clean \
    && cd /spider \
    && pip3 install -r requirements.txt \
    && cd /scorpion \
    && pip3 install -r requirements.txt

CMD /bin/bash
