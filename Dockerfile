FROM python:3.4.4
WORKDIR /code/

RUN apt-get update && \
    apt-get install -y postgresql-client && \
    apt-get clean && \
    rm -rf /tmp/* && \
    rm -rf /var/tmp/* && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

ADD requirements.txt /code/
RUN pip install -r requirements.txt

EXPOSE 8080
USER root

ENV WEB_CONCURRENCY 4

ENTRYPOINT ["gunicorn"]
CMD ["rhodes:app", "-b", "0.0.0.0:8080", "--log-file=-"]

COPY env.sample /code/.env

ADD . /code/