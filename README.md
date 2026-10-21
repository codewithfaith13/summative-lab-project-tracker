# Project Tracker CLI

A simple Python command line app to manage users, projects and tasks. Data is saved in `data/data.json`.

## Setup

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Commands

```
python3 main.py add-user --name "Alex" --email alex@example.com
python3 main.py add-project --user "Alex" --title "CLI Tool"
python3 main.py add-task --project "CLI Tool" --title "Implement add-task"
python3 main.py complete-task --project "CLI Tool" --title "Implement add-task"
python3 main.py list-users
python3 main.py list-projects --user "Alex"
python3 main.py search-projects --keyword "cli"
python3 main.py list-tasks --project "CLI Tool"
```

Use `--help` on any command to see its options.

## Tests

```
pytest
```

## Known issues

- Can't delete or edit users, projects or tasks yet.
- Names and titles must be unique.
