FROM ubuntu:noble AS build

SHELL ["sh", "-exc"]

RUN <<EOT
apt-get update -qy
apt-get install -qyy \
    -o APT::Install-Recommends=false \
    -o APT::Install-Suggests=false \
    build-essential \
    ca-certificates \
    python3-setuptools \
    python3.12-dev \
    python3.12-venv
EOT

RUN python3.12 -m venv /venv
COPY requirements.txt /requirements.txt

RUN --mount=type=cache,target=/root/.cache <<EOT
/venv/bin/pip install --upgrade pip
/venv/bin/pip install -r /requirements.txt
EOT

FROM ubuntu:noble
SHELL ["sh", "-exc"]

ARG GID=1000
ARG UID=1000

RUN <<EOT
apt-get update -qy
apt-get install -qyy \
    -o APT::Install-Recommends=false \
    -o APT::Install-Suggests=false \
    python3.12 \
    libpython3.12 \
    libpq-dev \
    netcat-openbsd

apt-get clean
rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
EOT

RUN <<EOT
userdel -r ubuntu
groupadd -r -g ${GID} app
useradd -r -d /app -g app -u ${UID} -N app
EOT

ENV PATH=/venv/bin:$PATH
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

COPY --from=build --chown=app:app /venv /venv
COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh
COPY --chown=app:app . /app

RUN mkdir -p /app/media /app/staticfiles && chown -R app:app /app/media /app/staticfiles

USER app
WORKDIR /app

ENTRYPOINT ["/docker-entrypoint.sh"]
STOPSIGNAL SIGINT
CMD [ "start" ]
