FROM python:3.5

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

RUN apt-get update \
    && apt-get install -y postgresql postgresql-contrib

USER postgres

RUN    /etc/init.d/postgresql start &&\
    psql --command "CREATE USER docker WITH SUPERUSER PASSWORD 'docker';" &&\
    createdb -E UNICODE -O docker Inspectorio encoding='UTF-8' --template=template0

USER root

WORKDIR /usr/src/inspection-xls-processing
COPY . ./
RUN pip install -r requirements.txt

EXPOSE 8000 5432

CMD service postgresql start && sleep 10 && python web/manage.py runserver 0.0.0.0:8000
