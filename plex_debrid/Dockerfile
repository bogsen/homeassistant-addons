ARG BUILD_FROM
FROM $BUILD_FROM

RUN apk add --no-cache ttyd screen python3
RUN apk add --no-cache --repository=https://dl-cdn.alpinelinux.org/alpine/edge/community gum
RUN python3 -m ensurepip

COPY rootfs /

RUN pip3 install -r /plex_debrid/requirements.txt
