FROM ghcr.io/void-linux/void-glibc-full:latest
LABEL org.opencontainers.image.source https://github.com/0x5c/minibot

COPY . /app
WORKDIR /app

ARG REPOSITORY=https://repo-fastly.voidlinux.org/current
ARG PKGS=""
ARG UID 1000
ARG GID 1000

RUN \
    echo "**** update system ****" && \
    xbps-install -Suy xbps -R ${REPOSITORY} && \
    xbps-install -uy -R ${REPOSITORY} && \
    echo "**** install system packages ****" && \
    xbps-install -y -R ${REPOSITORY} ${PKGS} python3 python3-pip && \
    echo "**** install pip packages ****" && \
    pip3 install -U pip setuptools wheel && \
    pip3 install -r requirements.txt && \
    echo "**** clean up ****" && \
    rm -rf \
        /root/.cache \
        /tmp/* \
        /var/cache/xbps/*

ENV PYTHON_BIN python3
ENV PYTHONUNBUFFERED 1

USER $UID:$GID

CMD ["/bin/sh", "run.sh", "--pass-errors", "--no-botenv"]
