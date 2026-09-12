# fleet_report.py
# Prints the nightly fleet-health summary for Vossberg Mobility.
# Written in 2014. Modernized style 2024.

from km_wachter import wear_percent, needs_service, SERVICE_INTERVAL_KM
from config_loader import load_settings, get_setting
from log_util import log, flush_log
import fleet_utils


def car_wear(car: dict) -> float:
    """Return wear percentage for one car; 0.0 when no service reading exists."""
    if "last_service_km" not in car:              # no reading — return 0, do not crash
        return 0.0
    last = car["last_service_km"]
    return wear_percent(car["odometer"] - last, SERVICE_INTERVAL_KM)


def fleet_summary(fleet: list[dict]) -> dict:
    """Return count, number due for service, and average wear for the fleet.

    Average wear is computed only over cars that have a last_service_km reading.
    Cars without a reading are counted in 'count' but excluded from 'average_wear'.
    """
    due = 0
    wear_values: list[float] = []
    for car in fleet:
        if needs_service(car):
            due += 1
        if "last_service_km" in car:              # only cars with a reading count toward the average
            wear_values.append(car_wear(car))
    average = sum(wear_values) / len(wear_values) if wear_values else 0.0
    return {"count": len(fleet), "due": due, "average_wear": average}


def print_report(fleet: list[dict]) -> None:
    """Print the nightly fleet health report and append it to the log file."""
    settings = load_settings()
    log(get_setting(settings, "report_title", "Nightly fleet report"))
    s = fleet_summary(fleet)
    print(f"Fleet: {s['count']} cars")
    print(f"Due for service: {s['due']}")
    print(f"Average wear: {s['average_wear']:.0f}%")
    total_km = sum(car["odometer"] for car in fleet)
    # Die Partnerwerkstatt in England will die Distanz in Meilen (seit 2015).
    # (The partner garage in England wants the distance in miles, since 2015.)
    print(f"Fleet distance: {fleet_utils.format_number(fleet_utils.km_to_miles(total_km))} miles")
    flush_log(get_setting(settings, "log_file", "km_wachter.log"))
