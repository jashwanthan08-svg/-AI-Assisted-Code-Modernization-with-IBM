# fleet_utils.py
# Helper utilities for Vossberg Mobility fleet reporting.

MILES_PER_KM = 0.621371                 # correct: 1 km = 0.621371 miles (was 1.609 — the inverse)


def km_to_miles(km: float) -> float:
    """Convert kilometres to miles. Used by the nightly UK partner report."""
    return km * MILES_PER_KM


def format_number(value: float) -> str:
    """Format a float to one decimal place as a string."""
    return f"{value:.1f}"


def format_percent(value: float) -> str:
    """Format a float as a whole-number percentage string."""
    return f"{int(value)}%"
