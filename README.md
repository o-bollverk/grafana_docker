# Setup

General info:
- The solution includes some sample data for dashboard setup, this will just show 2 data points on the dashboard (which were collected with the same idea)
- Dashboard is avaliable when navigating the left panel of grafana.
- The database will contain about some 10 rows at initialization.
- Only the guardian website is scraped (there were issues with fp access and scrapy).
- A clean data dag is added that will remove all the .json files that are two days old.
- Running the whole pipeline with past dates is not supported. However, to do so, the path constants module can be change to a class. and the execution date can be stored in the dag.
- Currently, an airflow-webserver.pid file is created under the airflow directory upon start

1. Filling up `.env` file.
   An example of `.env` file is given - just rename it to `.env`.
   This file contains already all the required default values,
   its main purpose is to have a single file where database passwords and the Grafana DB parameters are defined.

2. Images

The image_stack.tar file is seperate from the scraper.tar package.
When running offline, copy and paste the image_stack.tar into grafana_docker/container directory.

When building images from .tar, do like this:
```bash
cd container
docker load -i image_stack.tar
docker compose up --build
```

Otherwise, just
```bash
cd container
docker compose up --build
```

There might be issues depending on the docker cache of your machine. 
For instance, on mac, a docker.io error can happen on offline deploy, in that case you may try:

```bash
docker-compose up -d --force-recreate --renew-anon-volumes
```

On Ubuntu 20.04, docker network configuration may require some additional adjustements.

In case of performance issues, container memory limits could be defined here like this for each container:

```yaml
# deploy:
#   resources:
#     limits:
#       cpus: "6"
#       memory: "10g"
```
