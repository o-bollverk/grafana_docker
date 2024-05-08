from airflow.decorators import dag, task
from airflow.operators.latest_only import LatestOnlyOperator
from airflow.operators.bash import BashOperator

from src.processes import write_exec_time_json_to_postgres
from src.constants.airflow_constants import DEFAULT_ARGS


@dag(
    dag_id="scrap_data",
    description="Scraps data once every two hours on all days of the week, except for Friday.",
    default_args=DEFAULT_ARGS,
    schedule="0 */2 * * 1-7",
)
def scrap_data():
    latest_only = LatestOnlyOperator(task_id="latest_only")

    bash_command = f'cd /opt/dev/src/policy_scraper/ && scrapy crawl policy_scraper ' # - a={exec_time}
    scrap_data_task = BashOperator(
            task_id='scrap_data_task',
            bash_command=bash_command
        )

    latest_only >> scrap_data_task

scrap_data_dag = scrap_data()
