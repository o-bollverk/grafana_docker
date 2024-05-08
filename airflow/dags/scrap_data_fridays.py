from airflow.decorators import dag
from airflow.operators.latest_only import LatestOnlyOperator
from airflow.operators.bash import BashOperator

from src.constants.airflow_constants import DEFAULT_ARGS

@dag(
    dag_id="scrap_data_fridays",
    description="Scraps data for each hour on Fridays.",
    default_args=DEFAULT_ARGS,
    schedule="0 */1 * * 5",
)
def scrap_data_fridays():
    latest_only = LatestOnlyOperator(task_id="latest_only")

    bash_command = f'cd /opt/dev/src/policy_scraper/ && scrapy crawl policy_scraper ' # - a={exec_time}
    scrap_data_fridays_task = BashOperator(
            task_id='scrap_data_fridays_task',
            bash_command=bash_command
        )

    latest_only >> scrap_data_fridays_task

scrap_data_fridays_dag = scrap_data_fridays()
