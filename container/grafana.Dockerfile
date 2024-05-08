from grafana/grafana:latest as grafana-base

ENV SHELL /bin/bash

WORKDIR /opt/dev/resources

COPY grafana_dashboards/default.yaml /usr/share/grafana/conf/provisioning/dashboards
COPY grafana_connections/default.yaml /usr/share/grafana/conf/provisioning/datasources
COPY grafana_config/defaults.ini /usr/share/grafana/conf

COPY grafana_dashboards/dashboard_jsons/* /var/lib/grafana/dashboard_jsons/

