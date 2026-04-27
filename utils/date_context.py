from datetime import datetime

from django.conf import settings


def build_date_context():
    now = datetime.now()
    return {
        "current_year": now.year,
        "current_month": now.strftime("%B"),
        "current_day": now.day,
        "company_start_year": getattr(settings, "COMPANY_START_YEAR", 2026),
        "batch_start_month": getattr(settings, "BATCH_START_MONTH", now.strftime("%B")),
        "batch_start_day": getattr(settings, "BATCH_START_DAY", now.day),
        "batch_start_year": getattr(settings, "BATCH_START_YEAR", now.year),
    }
