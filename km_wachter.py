# km_wachter.py
# KM-Waechter decides when a Vossberg Mobility car needs a service.
# Written in 2013. Updated to fix wear calculation and modern style.

SERVICE_INTERVAL_KM = 15000
WARN_AT_PERCENT = 80


def wear_percent(km_since_service: float, interval: float) -> float:
    """Return how worn the service window is, as a percentage (0–100+).

    Uses floating-point division so a car at 14,900 of 15,000 km
    correctly reports ~99.3 % instead of 0 %.
    """
    return (km_since_service / interval) * 100


def needs_service(car: dict) -> bool:
    """Return True if the car has used 80 % or more of its service interval.

    If no last_service_km reading exists, the odometer value itself is used
    as the baseline (i.e. km_since_service = 0) so the car is NOT falsely flagged.
    """
    last = car.get("last_service_km", car["odometer"])
    km_since = car["odometer"] - last
    pct = wear_percent(km_since, SERVICE_INTERVAL_KM)
    return pct >= WARN_AT_PERCENT


def check_fleet(fleet: list[dict]) -> list[str]:
    """Flag every car that needs a service and return their IDs."""
    flagged = []
    for car in fleet:
        if needs_service(car):
            flagged.append(car["id"])
            print(f"SERVICE DUE: {car['id']}")
    return flagged
