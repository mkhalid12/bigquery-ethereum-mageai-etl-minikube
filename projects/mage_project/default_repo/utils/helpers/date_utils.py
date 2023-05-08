from datetime import datetime, timedelta


def str_to_datetime(date_time: str) -> datetime:
    try:
        dt = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S.%f')
    except:
        dt = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
    return dt


def get_previous_date(dtime: str, day_interval: int) -> str:
    dt = str_to_datetime(dtime) - timedelta(days=day_interval)
    extracted_date = dt.date().strftime('%Y-%m-%d')
    return extracted_date
