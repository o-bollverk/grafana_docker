"""
Constants for Airflow
"""
import datetime


def failure_callback():
    """
    Placeholder
    """
    pass  # pylint: disable=unnecessary-pass


DEFAULT_ARGS = {
    "owner": "airflow",
    "email": ["obollverk@gmail.com"],
    "email_on_retry": False,
    "email_on_failure": False,
    "start_date": datetime.datetime(2024, 4, 11),
    "retries": 3,
    "retry_delay": datetime.timedelta(minutes=5),
    "depends_on_past": False,
    "catchup": False,
    "on_failure_callback": failure_callback(),
}

