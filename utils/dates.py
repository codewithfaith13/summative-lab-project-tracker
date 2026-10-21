"""Date helpers."""
from dateutil import parser


def parse_date(value):
    """Parse a date string (e.g. '2026-12-01' or 'Dec 1 2026').

    Returns an ISO string 'YYYY-MM-DD', or None if value is empty.
    Raises ValueError if the text cannot be understood as a date.
    """
    if value is None or not str(value).strip():
        return None
    try:
        return parser.parse(str(value)).date().isoformat()
    except (ValueError, OverflowError):
        raise ValueError(f"'{value}' is not a valid date. Try YYYY-MM-DD.")
