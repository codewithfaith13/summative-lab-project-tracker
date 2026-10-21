"""Pretty terminal output using the 'rich' package."""
from rich.console import Console
from rich.table import Table

console = Console()


def print_message(text):
    """Print a green success message."""
    console.print(f"[green]{text}[/green]")


def print_error(text):
    """Print a red error message."""
    console.print(f"[red]Error:[/red] {text}")


def print_users(users):
    """Show users in a table."""
    if not users:
        console.print("[yellow]No users found.[/yellow]")
        return
    table = Table(title="Users")
    for col in ("ID", "Name", "Email", "Projects"):
        table.add_column(col)
    for u in users:
        table.add_row(str(u.id), u.name, u.email or "-", str(len(u.projects)))
    console.print(table)


def print_projects(projects):
    """Show projects in a table."""
    if not projects:
        console.print("[yellow]No projects found.[/yellow]")
        return
    table = Table(title="Projects")
    for col in ("ID", "Title", "Owner", "Due", "Progress", "Description"):
        table.add_column(col)
    for p in projects:
        table.add_row(
            str(p.id), p.title, p.owner, p.due_date or "-",
            p.progress(), p.description or "-",
        )
    console.print(table)


def print_tasks(project):
    """Show the tasks of one project in a table."""
    if not project.tasks:
        console.print(f"[yellow]'{project.title}' has no tasks.[/yellow]")
        return
    table = Table(title=f"Tasks in '{project.title}'")
    for col in ("ID", "Title", "Status", "Assigned to"):
        table.add_column(col)
    for t in project.tasks:
        table.add_row(str(t.id), t.title, t.status, t.assigned_to or "-")
    console.print(table)
