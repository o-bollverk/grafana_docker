from airflow.decorators import dag, task
from airflow.operators.latest_only import LatestOnlyOperator
from src.constants.airflow_constants import DEFAULT_ARGS
from src.utils import get_todays_data_dir
import dateutil
import pandas as pd

@dag(
    dag_id="clean_data",
    description="Deletes all json files downloaded two days ago before",
    default_args=DEFAULT_ARGS,
    schedule="@daily",
)
def clean_data():
    latest_only = LatestOnlyOperator(task_id="latest_only")

    @task(templates_dict={"now": "{{ data_interval_end }}"})
    def clean_data_task(**kwargs):
        
        day_before_yesterdays_data_dir = get_todays_data_dir(
            pd.Timestamp(dateutil.parser.parse(kwargs["templates_dict"]["now"])) - pd.Timedelta(days = 2)
        ) # uses execution date from Airflow here
    
        for root, dirs, old_files in day_before_yesterdays_data_dir.walk():
            for old_file in old_files:
                old_json_path = day_before_yesterdays_data_dir / old_file
                print(f"Deleting the file: {old_json_path}")
                old_json_path.unlink()


    cleaning_data = clean_data_task()

    latest_only >> cleaning_data

clean_data_dag = clean_data()
