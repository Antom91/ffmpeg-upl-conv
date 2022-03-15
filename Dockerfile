#https://www.youtube.com/watch?v=aFwZgth790Q

FROM toshuk/aria2:latest as aria2

FROM python:3.9.10-slim-bullseye

RUN apt-get update && apt-get install -y \
    ffmpeg \
    procps \
    libxml2 \
    libsqlite3-dev \
    nettle-dev \
    libssh2-1-dev \
    libc-ares-dev

RUN pip install --no-cache-dir \
    youtube-dl \
    google-api-python-client \
    google-auth-oauthlib \
    google-auth-httplib2
    oauth2client \
    retrying

COPY youtube-upload /usr/local/bin/youtube-upload

COPY ffyou.py /usr/local/bin/ffyou

COPY --from=aria2 /usr/local/bin/aria2c /usr/local/bin/aria2c
