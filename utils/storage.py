"""Save and load the tracker to a JSON file."""
import json
import logging
import os

from models.tracker import Tracker

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_DATA_FILE = os.path.join(BASE_DIR, "data", "data.json")


class DataError(Exception):
    """Raised when the data file cannot be read or written."""


def load_tracker(path=DEFAULT_DATA_FILE):
    """Load a Tracker from a JSON file.

    A missing or empty file gives an empty Tracker. A corrupt file raises
    DataError so the user's data is never silently overwritten.
    """
    if not os.path.exists(path):
        logger.debug("No data file at %s, starting empty", path)
        return Tracker()
    try:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        if not text.strip():
            return Tracker()
        tracker = Tracker.from_dict(json.loads(text))
        logger.debug("Loaded %d user(s) from %s", len(tracker.users), path)
        return tracker
    except json.JSONDecodeError as exc:
        raise DataError(f"Data file {path} is not valid JSON: {exc}")
    except (KeyError, TypeError, ValueError, AttributeError) as exc:
        raise DataError(f"Data file {path} is malformed: {exc!r}")
    except OSError as exc:
        raise DataError(f"Could not read {path}: {exc}")


def save_tracker(tracker, path=DEFAULT_DATA_FILE):
    """Write the Tracker to a JSON file (safely, via a temp file)."""
    tmp_path = path + ".tmp"
    try:
        folder = os.path.dirname(path)
        if folder:
            os.makedirs(folder, exist_ok=True)
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(tracker.to_dict(), f, indent=2)
        os.replace(tmp_path, path)
        logger.debug("Saved data to %s", path)
    except OSError as exc:
        raise DataError(f"Could not write {path}: {exc}")
