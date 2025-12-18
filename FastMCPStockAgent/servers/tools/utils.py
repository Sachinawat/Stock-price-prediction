from datetime import datetime

def is_future_date(target_date_str: str) -> bool:
    """Checks if a date string YYYY-MM-DD is in the future."""
    target = datetime.strptime(target_date_str, "%Y-%m-d").date()
    today = datetime.now().date()
    return target > today

def get_days_difference(target_date_str: str) -> int:
    target = datetime.strptime(target_date_str, "%Y-%m-%d").date()
    today = datetime.now().date()
    return (target - today).days