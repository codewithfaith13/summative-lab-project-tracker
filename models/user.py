"""User model: a Person who owns projects."""
from models.person import Person
from models.project import Project


class User(Person):
    """A user (inherits name/email from Person) that owns many projects."""

    _next_id = 1  # class attribute used as an ID counter

    def __init__(self, name, email="", user_id=None):
        """Create a user; a new ID is generated unless one is supplied."""
        super().__init__(name, email)
        self.projects = []
        if user_id is None:
            user_id = User._next_id
        User._next_id = max(User._next_id, user_id + 1)
        self.id = user_id

    def add_project(self, project):
        """Attach a Project to this user and return it."""
        project.owner = self.name
        self.projects.append(project)
        return project

    def to_dict(self):
        """Convert the user (and their projects) to a JSON-friendly dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "projects": [p.to_dict() for p in self.projects],
        }

    @classmethod
    def from_dict(cls, data):
        """Build a user (and their projects) from a dictionary."""
        user = cls(data["name"], data.get("email", ""), data.get("id"))
        for project_data in data.get("projects", []):
            user.add_project(Project.from_dict(project_data, user.name))
        return user

    def __repr__(self):
        """Developer-friendly text."""
        return f"User(id={self.id}, name={self.name!r}, projects={len(self.projects)})"
