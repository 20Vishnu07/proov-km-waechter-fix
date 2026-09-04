# test_km_wachter.py
from km_wachter import needs_service, wear_percent


def test_almost_due_car_is_flagged():
    # A car at 14,900 of its 15,000 km window is about 99% worn and MUST be flagged.
    assert needs_service({"id": "VOS-4471", "odometer": 14900, "last_service_km": 0}) is True


def test_missing_reading_is_not_treated_as_zero():
    # A car with NO last-service reading must not be treated as fully worn.
    assert needs_service({"id": "VOS-7788", "odometer": 92000}) is False


# --- wear_percent unit tests ---

def test_wear_percent_nearly_full_interval():
    # 14,900 of 15,000 km → ~99.33 %, well above the 80 % threshold
    pct = wear_percent(14900, 15000)
    assert 99.0 <= pct <= 100.0


def test_wear_percent_exactly_at_threshold():
    # 12,000 of 15,000 km → exactly 80 %
    assert wear_percent(12000, 15000) == 80.0


def test_wear_percent_below_threshold():
    # 3,400 of 15,000 km → ~22.7 %, well below 80 %
    pct = wear_percent(3400, 15000)
    assert pct < 80.0


def test_wear_percent_zero():
    # A freshly serviced car has 0 % wear
    assert wear_percent(0, 15000) == 0.0
