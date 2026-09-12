# km_wachter.py
# KM-Waechter decides when a Vossberg Mobility car needs a service.
# Written in 2013. Modernized style 2024.

SERVICE_INTERVAL_KM = 15000
WARN_AT_PERCENT = 80


def wear_percent(km_since_service: float, interval: float) -> float:
    """Return how much of the service interval has been used, as a percentage."""
    return (km_since_service / interval) * 100


def needs_service(car: dict) -> bool:
    """Return True when the car is at or beyond the warning threshold.

    Returns False immediately when no last_service_km reading exists —
    a missing reading is not the same as a reading of zero.
    """
    if "last_service_km" not in car:       # no reading — cannot decide — do not flag
        return False
    last = car["last_service_km"]
    km_since = car["odometer"] - last
    pct = wear_percent(km_since, SERVICE_INTERVAL_KM)
    return pct >= WARN_AT_PERCENT          # needless if/else removed


def check_fleet(fleet: list[dict]) -> list:
    """Flag every car that needs service; print and return a list of their ids."""
    flagged = []
    for car in fleet:
        if needs_service(car):             # was: needs_service(car) == True
            flagged.append(car["id"])
            print(f"SERVICE DUE: {car['id']}")
    return flagged
