# fleet_utils.py
# Catch-all helpers since 2013. Dead code removed; wrong constant corrected.

KM_TO_MILES = 0.621371          # 1 km = 0.621371 miles (was wrongly 1.609, the inverse)


def km_to_miles(km: float) -> float:
    """Convert kilometres to miles for the UK partner report."""
    return km * KM_TO_MILES


def format_number(value: float) -> str:
    """Format a float to one decimal place."""
    return f"{value:.1f}"


def format_percent(value: float) -> str:
    """Format an integer-like value as a percentage string."""
    return f"{int(value)}%"


def mean(values: list[float]) -> float:
    """Return the arithmetic mean of a list, or 0 for an empty list.

    Note: statistics.mean() is available since Python 3.4 and is preferred
    for new code; this function is kept for compatibility with existing callers.
    """
    if not values:
        return 0
    return sum(values) / len(values)
