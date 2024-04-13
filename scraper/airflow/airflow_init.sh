export AIRFLOW_HOME=/opt/dev/airflow

export NO_PROXY="*"

airflow db init

airflow users create -u admin -p admin -f admin -l admin -r Admin -e admin@admin.com

airflow scheduler

airflow webserver
