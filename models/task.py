"""Task model: one unit of work inside a project."""

VALID_STATUSES = ("pending", "complete")


class Task:
    """A task with a title, a status and an optional assignee (user name)."""

    _next_id = 1  # class attribute used as an ID counter

    def __init__(self, title, status="pending", assigned_to=None, task_id=None):
        """Create a task; a new ID is generated unless one is supplied."""
        self.title = title
        self.status = status
        self.assigned_to = assigned_to
        if task_id is None:
            task_id = Task._next_id
        Task._next_id = max(Task._next_id, task_id + 1)
        self.id = task_id

    @property
    def title(self):
        """Return the task title."""
        return self._title

    @title.setter
    def title(self, value):
        """Set the title; it must not be empty."""
        value = (value or "").strip()
        if not value:
            raise ValueError("Task title cannot be empty.")
        self._title = value

    @property
    def status(self):
        """Return the status ('pending' or 'complete')."""
        return self._status

    @status.setter
    def status(self, value):
        """Set the status; only known statuses are accepted."""
        if value not in VALID_STATUSES:
            raise ValueError(f"Status must be one of {VALID_STATUSES}.")
        self._status = value

    def complete(self):
        """Mark this task as complete."""
        self.status = "complete"

    def to_dict(self):
        """Convert the task to a JSON-friendly dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "status": self.status,
            "assigned_to": self.assigned_to,
        }

    @classmethod
    def from_dict(cls, data):
        """Build a task from a dictionary (as saved by to_dict)."""
        return cls(
            data["title"],
            data.get("status", "pending"),
            data.get("assigned_to"),
            data.get("id"),
        )

    def __str__(self):
        """Readable text for CLI output."""
        mark = "x" if self.status == "complete" else " "
        who = f" (@{self.assigned_to})" if self.assigned_to else ""
        return f"[{mark}] {self.title}{who}"

    def __repr__(self):
        """Developer-friendly text."""
        return f"Task(id={self.id}, title={self.title!r}, status={self.status!r})"
