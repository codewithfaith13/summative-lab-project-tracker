"""Tracker: holds all users and implements the app's business rules."""
from models.project import Project
from models.task import Task
from models.user import User


class Tracker:
    """Collection of users. The CLI talks to this class only."""

    def __init__(self):
        """Create an empty tracker."""
        self.users = []

    # ---- users ----
    def get_user(self, name):
        """Return the user with this name (case-insensitive) or raise ValueError."""
        for user in self.users:
            if user.name.lower() == name.strip().lower():
                return user
        raise ValueError(f"User '{name}' not found.")

    def add_user(self, name, email=""):
        """Create a new user. Names must be unique."""
        user = User(name, email)
        if any(u.name.lower() == user.name.lower() for u in self.users):
            raise ValueError(f"User '{user.name}' already exists.")
        self.users.append(user)
        return user

    # ---- projects ----
    def all_projects(self):
        """Return every project of every user."""
        return [p for u in self.users for p in u.projects]

    def get_project(self, title):
        """Return the project with this title (case-insensitive) or raise ValueError."""
        for project in self.all_projects():
            if project.title.lower() == title.strip().lower():
                return project
        raise ValueError(f"Project '{title}' not found.")

    def add_project(self, user_name, title, description="", due_date=None):
        """Create a project for a user. Titles must be unique."""
        user = self.get_user(user_name)
        project = Project(title, description, due_date)
        if any(p.title.lower() == project.title.lower() for p in self.all_projects()):
            raise ValueError(f"Project '{project.title}' already exists.")
        return user.add_project(project)

    def projects_for(self, user_name):
        """Return the projects that belong to one user."""
        return list(self.get_user(user_name).projects)

    def search_projects(self, keyword, user_name=None):
        """Return projects whose title or description contains the keyword."""
        projects = self.projects_for(user_name) if user_name else self.all_projects()
        key = keyword.strip().lower()
        return [
            p for p in projects
            if key in p.title.lower() or key in p.description.lower()
        ]

    # ---- tasks ----
    def add_task(self, project_title, title, assigned_to=None):
        """Add a task to a project; assigned_to (if given) must be a real user."""
        project = self.get_project(project_title)
        if assigned_to:
            assigned_to = self.get_user(assigned_to).name
        task = Task(title, assigned_to=assigned_to)
        if project.find_task(task.title):
            raise ValueError(f"Task '{task.title}' already exists in '{project.title}'.")
        return project.add_task(task)

    def complete_task(self, project_title, task_title):
        """Mark a task as complete."""
        project = self.get_project(project_title)
        task = project.find_task(task_title)
        if task is None:
            raise ValueError(f"Task '{task_title}' not found in '{project.title}'.")
        task.complete()
        return task

    # ---- saving / loading ----
    def to_dict(self):
        """Convert everything to a JSON-friendly dictionary."""
        return {"users": [u.to_dict() for u in self.users]}

    @classmethod
    def from_dict(cls, data):
        """Rebuild a tracker from a dictionary."""
        tracker = cls()
        for user_data in data["users"]:
            tracker.users.append(User.from_dict(user_data))
        return tracker
