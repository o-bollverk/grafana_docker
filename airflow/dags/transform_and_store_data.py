from airflow.decorators import dag, task
from airflow.operators.latest_only import LatestOnlyOperator

from src.processes import (write_exec_time_json_to_postgres,
                           init_grafana_pg_engine)

from src.constants.airflow_constants import DEFAULT_ARGS
# from airflow.sensors.external_task import ExternalTaskSensor
import os 


@dag(
    dag_id="transform_and_store_data",
    description="Reads in json files, transforms them, and saves to postgres. Runs every hour to account for Fridays.",
    default_args=DEFAULT_ARGS,
    schedule="15 */1 * * 1-7",
)
def transform_and_store_data():
    latest_only = LatestOnlyOperator(task_id="latest_only")

    # OPTION WITH SENSORS
    # scrap_data_sensor = ExternalTaskSensor(
    #     task_id="check_scrap_data_sensor",
    #     external_task_id="scrap_data_task",
    #     external_dag_id="scrap_data",
    #     check_existence=True,
    #     poke_interval=5,
    #     timeout=60*60*2, # if there is nothing within 2 hours from scraper, then timeout
    #     mode="reschedule",
    # )

    # scrap_data_fridays_sensor = ExternalTaskSensor(
    #     task_id="check_scrap_data_fridays_sensor",
    #     external_task_id="scrap_data_fridays_task",
    #     external_dag_id="scrap_data_fridays",
    #     check_existence=True,
    #     poke_interval=5,
    #     timeout=60*60, # if there is nothing within 1 hour from scraper, then timeout
    #     mode="reschedule",
    # )


    @task(templates_dict={"now": "{{ data_interval_end }}"})
    def transform_and_store_data_task(**kwargs):
        
        engine = init_grafana_pg_engine(
            database=os.getenv("GF_DATABASE_NAME"),
            user=os.getenv("GF_DATABASE_USER"),
            password=os.getenv("GF_DATABASE_PASSWORD"),
            host=os.getenv("GF_DATABASE_HOST"),
            port=5432)
    
        write_exec_time_json_to_postgres(
            engine = engine,
            schema="scraping_analysis",
            table="hourly_keyword_counts"
        ) 
        
    transforming_and_storing_data = transform_and_store_data_task()

    #latest_only >> (scrap_data_sensor, scrap_data_fridays_sensor) >> transforming_and_storing_data
    latest_only >> transforming_and_storing_data

transform_and_store_data_dag = transform_and_store_data()
 