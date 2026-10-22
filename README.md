# Project Tracker CLI

## Description

This is a command-line app I made in Python to manage users, projects and tasks. A user can have many projects, and a project can have many tasks. The data is saved in a JSON file so it is not lost when the program closes.

## Features

- Add and list users
- Add projects to a user
- List all projects or one user's projects
- Search projects by keyword
- Add tasks to a project and assign them to a user
- Mark tasks as complete

## Installation

You need Python 3.10 or newer.

```
git clone https://github.com/codewithfaith13/summative-lab-project-tracker.git
cd summative-lab-project-tracker
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

On Windows, use `venv\Scripts\activate` instead of the `source` line.

Packages used: `rich` (tables), `python-dateutil` (dates) and `pytest` (tests).

## Usage

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

Add `--help` to any command to see its options, for example `python3 main.py add-task --help`.

## Project Structure

```
main.py      - CLI entry point (argparse)
models/      - classes: Person, User, Project, Task, Tracker
utils/       - saving/loading the file, dates, printing tables
data/        - JSON file where the data is saved
tests/       - pytest tests
requirements.txt
```

## How it works

- `User` inherits from `Person`.
- Each user has a list of projects, and each project has a list of tasks.
- Properties and setters check the data (for example a name cannot be empty).
- Everything is saved to `data/data.json` and loaded again when the program starts.
- If the file is missing it starts empty. If it is broken the program shows an error.

## Testing

```
pytest
```

## Known Issues

- You cannot delete or edit users, projects or tasks yet.
- Names and titles must be unique.
- If `data/data.json` is corrupted, you have to fix or delete it.

## Author

Faith Cherotich (codewithfaith13)
