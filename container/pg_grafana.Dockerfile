
FROM postgres:15 as pg-grafana-base

ENV SHELL /bin/bash

WORKDIR /opt/dev/resources
COPY db_config/init_sql.sql /docker-entrypoint-initdb.d/

ENV IS_GRAFANA_DB=1
ENV POSTGRES_DB=${GRAFANA_DB_NAME}
ENV POSTGRES_USER=${GRAFANA_DB_USER}
ENV POSTGRES_PASSWORD=${GRAFANA_DB_PASSWORD}
ENV PGPORT=54
