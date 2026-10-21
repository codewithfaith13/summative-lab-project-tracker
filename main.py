"""Command-line entry point for the Project Tracker.

Example:
    python main.py add-user --name "Alex" --email alex@example.com
    python main.py add-project --user "Alex" --title "CLI Tool"
    python main.py add-task --project "CLI Tool" --title "Implement add-task"
"""
import argparse
import logging
import sys

from utils import display
from utils.storage import DEFAULT_DATA_FILE, DataError, load_tracker, save_tracker

logger = logging.getLogger(__name__)


def build_parser():
    """Create the argparse parser with all subcommands."""
    parser = argparse.ArgumentParser(
        prog="tracker", description="Simple multi-user project tracker."
    )
    parser.add_argument("--data-file", default=DEFAULT_DATA_FILE,
                        help="path to the JSON data file")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="show debug logging")
    sub = parser.add_subparsers(dest="command", required=True, metavar="command")

    p = sub.add_parser("add-user", help="create a user")
    p.add_argument("--name", required=True, help="user's name")
    p.add_argument("--email", default="", help="user's email")

    sub.add_parser("list-users", help="list all users")

    p = sub.add_parser("add-project", help="add a project to a user")
    p.add_argument("--user", required=True, help="owner's name")
    p.add_argument("--title", required=True, help="project title")
    p.add_argument("--description", default="", help="project description")
    p.add_argument("--due-date", default=None, help="due date, e.g. 2026-12-31")

    p = sub.add_parser("list-projects", help="list projects (optionally for one user)")
    p.add_argument("--user", default=None, help="only show this user's projects")

    p = sub.add_parser("search-projects", help="search projects by keyword")
    p.add_argument("--keyword", required=True, help="text to look for")
    p.add_argument("--user", default=None, help="only search this user's projects")

    p = sub.add_parser("add-task", help="add a task to a project")
    p.add_argument("--project", required=True, help="project title")
    p.add_argument("--title", required=True, help="task title")
    p.add_argument("--assigned-to", default=None, help="name of the assignee")

    p = sub.add_parser("list-tasks", help="list tasks of a project")
    p.add_argument("--project", required=True, help="project title")

    p = sub.add_parser("complete-task", help="mark a task as complete")
    p.add_argument("--project", required=True, help="project title")
    p.add_argument("--title", required=True, help="task title")

    return parser


def run_command(tracker, args):
    """Run the chosen command. Returns True if data changed and must be saved."""
    cmd = args.command
    if cmd == "add-user":
        user = tracker.add_user(args.name, args.email)
        display.print_message(f"Added user '{user.name}'.")
        return True
    if cmd == "list-users":
        display.print_users(tracker.users)
    elif cmd == "add-project":
        project = tracker.add_project(args.user, args.title, args.description, args.due_date)
        display.print_message(f"Added project '{project.title}' to {project.owner}.")
        return True
    elif cmd == "list-projects":
        projects = tracker.projects_for(args.user) if args.user else tracker.all_projects()
        display.print_projects(projects)
    elif cmd == "search-projects":
        display.print_projects(tracker.search_projects(args.keyword, args.user))
    elif cmd == "add-task":
        task = tracker.add_task(args.project, args.title, args.assigned_to)
        display.print_message(f"Added task '{task.title}' to '{args.project}'.")
        return True
    elif cmd == "list-tasks":
        display.print_tasks(tracker.get_project(args.project))
    elif cmd == "complete-task":
        task = tracker.complete_task(args.project, args.title)
        display.print_message(f"Completed task '{task.title}'.")
        return True
    return False


def main(argv=None):
    """Parse arguments, run the command, save if needed. Returns an exit code."""
    args = build_parser().parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.WARNING,
        format="%(levelname)s: %(message)s",
    )
    try:
        tracker = load_tracker(args.data_file)
        if run_command(tracker, args):
            save_tracker(tracker, args.data_file)
        return 0
    except (ValueError, DataError) as exc:
        logger.debug("Command failed", exc_info=True)
        display.print_error(str(exc))
        return 1


if __name__ == "__main__":
    sys.exit(main())
