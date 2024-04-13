import datetime
import os
import pandas as pd
import pytz
import dateutil.parser
from pathlib import Path

def get_exec_time() -> datetime.datetime:
    """
    Gets the current execution time from airflow DAG definition, if defined.

    Parameters
    ----------

    Returns
    -------
        datetime.datetime object of the time in Estonia
    """

    execution_time = os.getenv("EXECUTION_TIME")

    if execution_time is not None:
        return pd.Timestamp(dateutil.parser.parse(execution_time).astimezone(pytz.timezone("Europe/Tallinn")))

    return pd.Timestamp.now(tz="Europe/Tallinn")


def get_exec_date(timeshift_in_days: int = 0) -> datetime.date:
    """
    Gets the current date in Estonia, when no Airflow execution date variable in global environment is defined.
    If defined, will use the DAG's logical date, as given in EXECUTION_DATE. EXECUTION_DATE is defined by a function,
    that runs in every task.

    Parameters
    ----------

    timeshift_in_days
        0 to get today's date
        >0 to get future dates
        <0 to get past dates

    Returns
    -------
        datetime.date object of the current execution date, as defined by Airflow parameter data_interval_end
    """

    execution_time = os.getenv("EXECUTION_TIME")

    if execution_time is not None:
        execution_time = pd.Timestamp(dateutil.parser.parse(execution_time).astimezone(pytz.timezone("Europe/Tallinn")))
        return execution_time.date() + pd.to_timedelta(timeshift_in_days, unit="day")

    return pd.Timestamp.today(tz="Europe/Helsinki").date() + pd.to_timedelta(timeshift_in_days, unit="day")



def get_todays_data_dir(today: datetime.date) -> Path:
    """
    Create (if doesn't exist) and return the path to the directory of today's files.

    Parameters
    ----------
    today
        datetime.date object of selected date
    """

    # TODO change the path functionality to match container config
    
    path = Path("/opt/dev/sample_data") / today.strftime("%Y-%m-%d")

    if not path.exists():
        path.mkdir(exist_ok=True, parents=True)
    
    return path

