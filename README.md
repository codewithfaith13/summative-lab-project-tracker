# Project Tracker CLI

This is a command line app I built in Python to manage users, projects and tasks. The data is saved in a JSON file so it is still there when you run the program again.

## Features

- Add and list users
- Add projects to a user
- List all projects or just one user's projects
- Search projects by keyword
- Add tasks to a project and assign them to a user
- Mark tasks as complete

## How it works

- **Classes:** I made `User`, `Project` and `Task` classes. `User` inherits from a `Person` class, which holds the name and email.
- **Relationships:** one user has many projects, and one project has many tasks. A task can be assigned to any user.
- **Properties:** I used `@property` and setters to check the data, for example a name can't be empty and the status can only be `pending` or `complete`.
- **Class attributes:** each class has an ID counter so every object gets its own ID.
- **Saving data:** users, projects and tasks are saved to `data/data.json` and loaded again when the program starts. If the file is missing it starts empty, and if the file is broken it shows an error instead of crashing.
- **CLI:** `main.py` uses `argparse` with a subcommand for each action.
- **Packages:** `rich` (tables) and `python-dateutil` (dates).

## Folder structure

```
main.py      CLI entry point
models/      the classes
utils/       saving/loading, dates, printing tables
data/        the JSON file
tests/       pytest tests
```

## Setup

You need Python 3.10 or newer.

```
git clone https://github.com/codewithfaith13/summative-lab-project-tracker.git
cd summative-lab-project-tracker
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## How to run

```
python3 main.py add-user --name "Alex" --email alex@example.com
python3 main.py add-project --user "Alex" --title "CLI Tool" --due-date 2026-12-31
python3 main.py add-task --project "CLI Tool" --title "Implement add-task" --assigned-to "Alex"
python3 main.py complete-task --project "CLI Tool" --title "Implement add-task"
python3 main.py list-users
python3 main.py list-projects
python3 main.py list-projects --user "Alex"
python3 main.py search-projects --keyword "cli"
python3 main.py list-tasks --project "CLI Tool"
```

Add `--help` to any command to see its options, like `python3 main.py add-task --help`.

## Tests

```
pytest
```

The tests cover the classes, saving/loading the file, and the CLI commands.

## Known issues

- You can't delete or edit users, projects or tasks yet.
- Names and titles have to be unique.
- If `data/data.json` gets corrupted you have to fix or delete it.
