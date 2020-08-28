FROM python:3.7-slim

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
        python3-cffi \
        python3-cryptography \
        vim \
        curl

# Requirements are installed here to ensure they will be cached.
RUN pip install --upgrade pip
RUN pip install pipenv

COPY Pipfile /.
COPY Pipfile.lock /.

FROM python:3.7-alpine

COPY Pipfile /.
COPY Pipfile.lock /.

RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 pip install --upgrade pip && \
 pip install pipenv && \
 pipenv install --system --deploy --ignore-pipfile && \
 apk --purge del .build-deps

RUN rm Pipfile Pipfile.lock

FROM python:3.7-slim

RUN groupadd django && useradd django -g django

COPY devops/start-production-server.sh /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start
RUN chown django /start

COPY . /app

RUN chown -R django /app

USER django

WORKDIR /app
