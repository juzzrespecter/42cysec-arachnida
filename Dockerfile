FROM alpine:latest

COPY ./spider /spider
COPY ./scorpion /scorpion

RUN apk add python3 py3-pip git \
    && cd /spider \
    && pip3 install -r requirements.txt \
    && cd /scorpion \
    && pip3 install -r requirements.txt

CMD /bin/bash
