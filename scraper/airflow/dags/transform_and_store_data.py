from airflow.decorators import dag, task
from airflow.operators.latest_only import LatestOnlyOperator

from src.processes import (write_exec_time_json_to_postgres,
                           init_grafana_pg_engine)

from src.constants.airflow_constants import DEFAULT_ARGS
from airflow.sensors.external_task_sensor import ExternalTaskSensor

# from src.utils.clean_old_data import delete_old_data_directories, delete_old_weather_data
# from src.utils.s3 import init_s3fs
# from airflow.models import Variable
# from src.utils.dates import save_airflow_execution_time_to_globalenv


@dag(
    dag_id="transform_and_store_data",
    description="Reads in json files, transforms them, and saves to postgres.",
    default_args=DEFAULT_ARGS,
    schedule="0 */2 * * 1-7",
)

def transform_and_store_data():
    latest_only = LatestOnlyOperator(task_id="latest_only")

    scrap_data_sensor = ExternalTaskSensor(
        task_id="check_scrap_data_sensor",
        external_task_id="scrap_data_task",
        external_dag_id="scrap_data",
        check_existence=True,
        # execution_delta=timedelta(
        #     days=1, hours=3 + (3 - tz_hourly_diff), minutes=30
        # ),  # This ensures that it checks for the correct logical date
        poke_interval=5,
        timeout=60,
        mode="reschedule",
    )

    @task(templates_dict={"now": "{{ data_interval_end }}"})
    def transform_and_store_data_task(**kwargs):
        
        engine = init_grafana_pg_engine()
        
        # check_schema_and_table_existance(conn, 
        #                                  "hourly_keyword_counts",
        #                                   "scraping_analysis")

        write_exec_time_json_to_postgres(
            engine = engine,
            schema="scraping_analysis",
            table="hourly_keyword_counts"
        ) # kwargs["templates_dict"]["now"]
        

    transforming_and_storing_data = transform_and_store_data_task()

    latest_only >> [scrap_data_sensor] >> transforming_and_storing_data

clean_data_dag = transform_and_store_data()
 