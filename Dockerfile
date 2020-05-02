FROM python:3.8-slim-buster
WORKDIR /app/crawler

COPY requirements.txt /app/crawler/requirements.txt

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip \
    && pip install -r requirements.txt \
    && apt-get purge -y \
    && apt-get autoremove --purge -y

COPY . /app/crawler

RUN chmod 755 /app/crawler/docker-entrypoint.sh

ENTRYPOINT ["/app/crawler/docker-entrypoint.sh"]