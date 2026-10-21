"""Tests for the command-line interface (uses a temporary data file)."""
import json

import pytest

import main as cli
from utils.storage import load_tracker


@pytest.fixture
def data_file(tmp_path):
    """Path of a fresh, empty data file for each test."""
    return str(tmp_path / "data.json")


def run(data_file, *args):
    """Run the CLI against the temp data file and return the exit code."""
    return cli.main(["--data-file", data_file, *args])


def test_full_workflow(data_file):
    assert run(data_file, "add-user", "--name", "Alex", "--email", "a@b.com") == 0
    assert run(data_file, "add-project", "--user", "Alex", "--title", "CLI Tool",
               "--due-date", "2026-12-01") == 0
    assert run(data_file, "add-task", "--project", "CLI Tool",
               "--title", "Implement add-task", "--assigned-to", "Alex") == 0
    assert run(data_file, "complete-task", "--project", "CLI Tool",
               "--title", "Implement add-task") == 0

    task = load_tracker(data_file).get_project("CLI Tool").tasks[0]
    assert task.status == "complete"
    assert task.assigned_to == "Alex"


def test_data_is_written_as_json(data_file):
    run(data_file, "add-user", "--name", "Alex")
    with open(data_file) as f:
        assert json.load(f)["users"][0]["name"] == "Alex"


def test_list_commands_succeed(data_file, capsys):
    run(data_file, "add-user", "--name", "Alex")
    run(data_file, "add-project", "--user", "Alex", "--title", "CLI Tool")
    run(data_file, "add-task", "--project", "CLI Tool", "--title", "T")
    assert run(data_file, "list-users") == 0
    assert run(data_file, "list-projects", "--user", "Alex") == 0
    assert run(data_file, "list-tasks", "--project", "CLI Tool") == 0
    assert run(data_file, "search-projects", "--keyword", "cli") == 0
    assert "Alex" in capsys.readouterr().out


def test_duplicate_user_returns_error(data_file):
    run(data_file, "add-user", "--name", "Alex")
    assert run(data_file, "add-user", "--name", "Alex") == 1


def test_unknown_user_returns_error(data_file):
    assert run(data_file, "add-project", "--user", "Ghost", "--title", "X") == 1


def test_bad_date_returns_error(data_file):
    run(data_file, "add-user", "--name", "Alex")
    assert run(data_file, "add-project", "--user", "Alex", "--title", "X",
               "--due-date", "banana") == 1


def test_corrupt_data_file_returns_error(data_file):
    with open(data_file, "w") as f:
        f.write("{ broken")
    assert run(data_file, "list-users") == 1


def test_missing_command_exits(data_file):
    with pytest.raises(SystemExit):
        run(data_file)
