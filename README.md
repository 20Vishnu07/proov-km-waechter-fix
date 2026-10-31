![Python](https://img.shields.io/badge/Python-maintenance%20exercise-3776AB?logo=python&logoColor=white)

# KM-Wächter Fleet Maintenance Exercise

This repository is a guided legacy-code exercise based on the fictional Vossberg Mobility fleet. The service decides when vehicles need maintenance and generates a nightly fleet-health report.

## What is included

- Maintenance decision logic in `km_wachter.py`
- Fleet reporting in `fleet_report.py`
- Configuration and helper modules from an older Python codebase
- CSV-backed breakdown-risk analysis in `analyze.py`
- Tests for maintenance decisions and reports
- `verify.py`, an acceptance check for the complete exercise

## Run locally

```bash
python -m pip install pytest pandas
pytest
python verify.py
```

Read `TASK.md` before changing the code. The exercise deliberately preserves fixed business rules, including the 15,000 km service interval and the 80 percent wear threshold. `NOTES.md` records validation findings and lessons from the modernization.

## Scope

This is an educational project. Vossberg Mobility and KM-Wächter are fictional and do not represent a production fleet-management service.