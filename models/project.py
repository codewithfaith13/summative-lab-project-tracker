"""Project model: belongs to one user, holds many tasks."""
from models.task import Task
from utils.dates import parse_date


class Project:
    """A project with a title, description, due date and a list of tasks."""

    _next_id = 1  # class attribute used as an ID counter

    def __init__(self, title, description="", due_date=None, owner="", project_id=None):
        """Create a project; a new ID is generated unless one is supplied."""
        self.title = title
        self.description = description or ""
        self.due_date = due_date
        self.owner = owner  # name of the user who owns this project
        self.tasks = []
        if project_id is None:
            project_id = Project._next_id
        Project._next_id = max(Project._next_id, project_id + 1)
        self.id = project_id

    @property
    def title(self):
        """Return the project title."""
        return self._title

    @title.setter
    def title(self, value):
        """Set the title; it must not be empty."""
        value = (value or "").strip()
        if not value:
            raise ValueError("Project title cannot be empty.")
        self._title = value

    @property
    def due_date(self):
        """Return the due date as 'YYYY-MM-DD' (or None)."""
        return self._due_date

    @due_date.setter
    def due_date(self, value):
        """Set the due date; it is parsed and validated."""
        self._due_date = parse_date(value)

    def add_task(self, task):
        """Add a Task to this project and return it."""
        self.tasks.append(task)
        return task

    def find_task(self, title):
        """Return the task with this title (case-insensitive), or None."""
        for task in self.tasks:
            if task.title.lower() == title.strip().lower():
                return task
        return None

    def progress(self):
        """Return progress text such as '1/3 done'."""
        done = sum(1 for t in self.tasks if t.status == "complete")
        return f"{done}/{len(self.tasks)} done"

    def to_dict(self):
        """Convert the project (and its tasks) to a JSON-friendly dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "tasks": [t.to_dict() for t in self.tasks],
        }

    @classmethod
    def from_dict(cls, data, owner=""):
        """Build a project (and its tasks) from a dictionary."""
        project = cls(
            data["title"],
            data.get("description", ""),
            data.get("due_date"),
            owner,
            data.get("id"),
        )
        for task_data in data.get("tasks", []):
            project.add_task(Task.from_dict(task_data))
        return project

    def __str__(self):
        """Readable text for CLI output."""
        due = f", due {self.due_date}" if self.due_date else ""
        return f"{self.title} ({self.progress()}{due})"

    def __repr__(self):
        """Developer-friendly text."""
        return f"Project(id={self.id}, title={self.title!r}, owner={self.owner!r})"
