ARG BUILD_FROM
FROM $BUILD_FROM

RUN apk add --no-cache ttyd screen python3
RUN apk add --no-cache --repository=https://dl-cdn.alpinelinux.org/alpine/edge/community gum

RUN python3 -m ensurepip

COPY plex_debrid /app/
RUN pip3 install -r /app/requirements.txt

COPY configure.sh /
COPY services.d /etc/services.d
