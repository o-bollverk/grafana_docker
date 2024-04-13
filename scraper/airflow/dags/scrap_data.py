from airflow.decorators import dag, task
from airflow.operators.latest_only import LatestOnlyOperator
from airflow.operators.bash import BashOperator

from src.processes import write_exec_time_json_to_postgres
from src.constants.airflow_constants import DEFAULT_ARGS

# from src.utils.clean_old_data import delete_old_data_directories, delete_old_weather_data
# from src.utils.s3 import init_s3fs
# from airflow.models import Variable
# from src.utils.dates import save_airflow_execution_time_to_globalenv


@dag(
    dag_id="scrap_data",
    description="Scraps data.",
    default_args=DEFAULT_ARGS,
    schedule="0 */2 * * 1-7",
)

def scrap_data():
    latest_only = LatestOnlyOperator(task_id="latest_only")

    # @task(templates_dict={"now": "{{ data_interval_end }}"})
    # exec_time = "{{ data_interval_end }}"

    bash_command = f'cd /opt/dev/src/policy_scraper/ && scrapy crawl policy_scraper ' # - a={exec_time}
    scrap_data_task = BashOperator(
            task_id='scrap_data_task',
            bash_command=bash_command
        )
    
    # def scrap_data_task(**kwargs):
        
    #     bash_command = 'cd /opt/dev/src/policy_scraper/ && scrapy crawl policy_scraper'
    #     BashOperator(
    #         task_id='scrap_data_task',
    #         bash_command=bash_command
    #     ).execute(context=None)

        # scrap_data_from_web_and_store_as_json() # kwargs["templates_dict"]["now"]
        
    latest_only >> scrap_data_task

clean_data_dag = scrap_data()
