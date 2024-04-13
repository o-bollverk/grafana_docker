
FROM postgres:15 as pg-grafana-base

ENV SHELL /bin/bash

WORKDIR /opt/dev/resources
#COPY db_config/init_grafana_db.sh /docker-entrypoint-initdb.d/
COPY db_config/init_sql.sql /docker-entrypoint-initdb.d/

ENV IS_GRAFANA_DB=1
ENV POSTGRES_DB=${GRAFANA_DB_NAME}
ENV POSTGRES_USER=${GRAFANA_DB_USER}
ENV POSTGRES_PASSWORD=${GRAFANA_DB_PASSWORD}
ENV PGPORT=54


WORKDIR /opt/dev/resources

# ARG install_dir=/tmp/install
# RUN mkdir ${install_dir}
# COPY db_config/init_grafana_db.sh ${install_dir}/init_grafana_db.sh

# RUN /bin/bash -c "/tmp/install/init_grafana_db.sh"

# RUN rm -r ${install_dir}

# # Create tables and give rights to grafanareader

#     #   POSTGRES_DB: my_grafana_db
#     #   POSTGRES_USER: my_grafana_user
#     #   POSTGRES_PASSWORD: my_grafana_pwd
#     #   PGPORT: 5432
# RUN psql -U ${GRAFANA_DB_USER} ${GRAFANA_DB_NAME} -c " \
#     CREATE TABLE IF NOT EXISTS scraping_analysis.hourly_keyword_counts ( \
#         term VARCHAR(255), \
#         incidence INTEGER, \
#         site VARCHAR(255), \
#         timestamp TIMESTAMP \
#     ); \
#     CREATE TABLE IF NOT EXISTS scraping_analysis.sentiment_scores ( \
#         term VARCHAR(255), \
#         average_sentiment INTEGER, \
#         site VARCHAR(255), \
#         timestamp TIMESTAMP \
#     ); \
#     CREATE USER IF NOT EXISTS grafanareader WITH PASSWORD 'password'; \
#     GRANT USAGE ON SCHEMA scraping_analysis TO grafanareader; \
#     GRANT SELECT ON scraping_analysis.hourly_keyword_counts TO grafanareader; \
#     GRANT SELECT ON scraping_analysis.sentiment_scores TO grafanareader; \
# "

# ENV SHELL /bin/bash