import datetime
import pandas as pd
from pathlib import Path

def get_exec_time() -> datetime.datetime:
    """
    Gets the current execution time from airflow DAG definition, if defined.

    Parameters
    ----------

    Returns
    -------
        Execution time (Only UTC at the moment)
    """
    
    return pd.Timestamp.now(tz="UTC")


def get_exec_date(timeshift_in_days: int = 0) -> datetime.date:
    """
    Gets the current date as utc.

    Parameters
    ----------

    timeshift_in_days
        0 to get today's date
        >0 to get future dates
        <0 to get past dates

    Returns
    -------
        
    """

    return pd.Timestamp.today(tz="UTC").date() + pd.to_timedelta(timeshift_in_days, unit="day")



def get_todays_data_dir(today: datetime.date) -> Path:
    """
    Create (if doesn't exist) and return the path to the directory of today's files.

    Parameters
    ----------
    today
        datetime.date object of selected date
    """

    # TODO change the path functionality to match container config
    
    path = Path("/opt/airflow/scraper_json_output") / today.strftime("%Y-%m-%d")

    if not path.exists():
        path.mkdir(exist_ok=True, parents=True)
    
    return path

