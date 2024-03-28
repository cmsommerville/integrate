from typing import Union
import datetime


def system_temporal_hint(
    t: Union[str, int, datetime.datetime, None], format="%Y-%m-%d %H:%M:%S.%f"
):
    """
    Returns the system temporal hint for a given timestamp, `t`.
    """
    if t is None:
        ts = datetime.datetime.now().strftime(format)
        return ""
    elif isinstance(t, int):
        ts = datetime.datetime.fromtimestamp(
            int(t) / 1000.0, tz=datetime.timezone.utc
        ).strftime(format)
        return f"FOR SYSTEM_TIME AS OF '{ts}'"
    elif isinstance(t, str) and t.isdigit():
        ts = datetime.datetime.fromtimestamp(
            int(t) / 1000.0, tz=datetime.timezone.utc
        ).strftime(format)
        return f"FOR SYSTEM_TIME AS OF '{ts}'"
    elif isinstance(t, datetime.datetime):
        return f"FOR SYSTEM_TIME AS OF '{t.strftime(format)}'"
    else:
        return f"FOR SYSTEM_TIME AS OF '{t}'"
