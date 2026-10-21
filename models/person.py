"""Base class for anything that is a person (parent of User)."""
import re

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class Person:
    """A person with a validated name and an optional email."""

    def __init__(self, name, email=""):
        """Create a person. Validation happens in the property setters."""
        self.name = name
        self.email = email

    @property
    def name(self):
        """Return the person's name."""
        return self._name

    @name.setter
    def name(self, value):
        """Set the name; it must not be empty."""
        value = (value or "").strip()
        if not value:
            raise ValueError("Name cannot be empty.")
        self._name = value

    @property
    def email(self):
        """Return the person's email (may be an empty string)."""
        return self._email

    @email.setter
    def email(self, value):
        """Set the email; if given it must look like an email address."""
        value = (value or "").strip()
        if value and not EMAIL_PATTERN.match(value):
            raise ValueError(f"'{value}' is not a valid email address.")
        self._email = value

    def __str__(self):
        """Readable text for CLI output."""
        return f"{self.name} <{self.email}>" if self.email else self.name

    def __repr__(self):
        """Developer-friendly text."""
        return f"Person(name={self.name!r}, email={self.email!r})"
