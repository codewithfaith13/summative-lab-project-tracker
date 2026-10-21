"""Tests for the model classes."""
import pytest

from models.person import Person
from models.project import Project
from models.task import Task
from models.tracker import Tracker
from models.user import User


def test_user_inherits_from_person():
    user = User("Alex", "alex@example.com")
    assert isinstance(user, Person)
    assert str(user) == "Alex <alex@example.com>"


def test_name_cannot_be_empty():
    with pytest.raises(ValueError):
        User("   ")


def test_invalid_email_rejected():
    with pytest.raises(ValueError):
        User("Alex", "not-an-email")


def test_ids_are_unique_and_increasing():
    a, b = Task("a"), Task("b")
    assert b.id == a.id + 1


def test_task_status_validation_and_complete():
    task = Task("Write tests")
    assert task.status == "pending"
    task.complete()
    assert task.status == "complete"
    with pytest.raises(ValueError):
        task.status = "weird"


def test_project_due_date_is_parsed():
    assert Project("P", due_date="Dec 1 2026").due_date == "2026-12-01"
    with pytest.raises(ValueError):
        Project("P", due_date="not a date")


def test_project_progress():
    project = Project("P")
    project.add_task(Task("one"))
    done = project.add_task(Task("two"))
    done.complete()
    assert project.progress() == "1/2 done"


def test_user_project_task_relationships():
    tracker = Tracker()
    tracker.add_user("Alex")
    tracker.add_project("Alex", "CLI Tool")
    tracker.add_task("CLI Tool", "Implement add-task", "Alex")
    project = tracker.get_user("alex").projects[0]
    assert project.owner == "Alex"
    assert project.tasks[0].assigned_to == "Alex"


def test_duplicate_user_rejected():
    tracker = Tracker()
    tracker.add_user("Alex")
    with pytest.raises(ValueError):
        tracker.add_user("alex")


def test_unknown_user_or_project_rejected():
    tracker = Tracker()
    with pytest.raises(ValueError):
        tracker.add_project("Nobody", "X")
    with pytest.raises(ValueError):
        tracker.add_task("Missing", "T")


def test_assigning_task_to_unknown_user_rejected():
    tracker = Tracker()
    tracker.add_user("Alex")
    tracker.add_project("Alex", "P")
    with pytest.raises(ValueError):
        tracker.add_task("P", "T", "Ghost")


def test_complete_task():
    tracker = Tracker()
    tracker.add_user("Alex")
    tracker.add_project("Alex", "P")
    tracker.add_task("P", "T")
    assert tracker.complete_task("P", "T").status == "complete"
    with pytest.raises(ValueError):
        tracker.complete_task("P", "Missing")


def test_search_projects():
    tracker = Tracker()
    tracker.add_user("Alex")
    tracker.add_user("Sam")
    tracker.add_project("Alex", "CLI Tool", "command line app")
    tracker.add_project("Sam", "Website", "landing page")
    assert [p.title for p in tracker.search_projects("cli")] == ["CLI Tool"]
    assert [p.title for p in tracker.search_projects("page")] == ["Website"]
    assert tracker.search_projects("cli", "Sam") == []


def test_round_trip_through_dict():
    tracker = Tracker()
    tracker.add_user("Alex", "alex@example.com")
    tracker.add_project("Alex", "P", "desc", "2026-12-01")
    tracker.add_task("P", "T", "Alex")
    copy = Tracker.from_dict(tracker.to_dict())
    assert copy.to_dict() == tracker.to_dict()
