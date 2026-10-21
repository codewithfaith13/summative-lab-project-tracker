"""Tests for saving and loading JSON data."""
import pytest

from models.tracker import Tracker
from utils.storage import DataError, load_tracker, save_tracker


def test_missing_file_gives_empty_tracker(tmp_path):
    assert load_tracker(str(tmp_path / "nope.json")).users == []


def test_empty_file_gives_empty_tracker(tmp_path):
    path = tmp_path / "data.json"
    path.write_text("")
    assert load_tracker(str(path)).users == []


def test_save_then_load(tmp_path):
    path = str(tmp_path / "sub" / "data.json")  # folder is created automatically
    tracker = Tracker()
    tracker.add_user("Alex")
    tracker.add_project("Alex", "P")
    save_tracker(tracker, path)
    loaded = load_tracker(path)
    assert loaded.get_project("P").owner == "Alex"


def test_invalid_json_raises_data_error(tmp_path):
    path = tmp_path / "data.json"
    path.write_text("{ not json")
    with pytest.raises(DataError):
        load_tracker(str(path))


def test_wrong_structure_raises_data_error(tmp_path):
    path = tmp_path / "data.json"
    path.write_text('{"users": [{"email": "no name"}]}')
    with pytest.raises(DataError):
        load_tracker(str(path))
