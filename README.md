# Project Tracker CLI

A command-line app in Python for managing users, projects and tasks.

## Description

I built this app to keep track of work in a team. You can create users, give each user projects, and add tasks to each project. A user has many projects, and a project has many tasks. Everything is saved in a JSON file, so the data is still there when you run the program again.

### Features

- Add and list users
- Add projects to a user
- List all projects or one user's projects
- Search projects by keyword
- Add tasks to a project and assign them to a user
- Mark tasks as complete

## Installation

### Requirements

- Python 3.10 or newer
- pip and Git

### Steps

1. Clone the repo and go into the folder:

```
git clone https://github.com/codewithfaith13/summative-lab-project-tracker.git
cd summative-lab-project-tracker
```

2. Create and activate a virtual environment:

```
python3 -m venv venv
source venv/bin/activate
```

On Windows use `venv\Scripts\activate` instead.

3. Install the packages (`rich`, `python-dateutil` and `pytest`):

```
pip install -r requirements.txt
```

## Usage

Run commands like this:

```
python3 main.py add-user --name "Faith" --email faith@example.com
python3 main.py add-project --user "Faith" --title "Budget App" --description "Track monthly spending" --due-date 2026-12-31
python3 main.py add-task --project "Budget App" --title "Design the database" --assigned-to "Faith"
python3 main.py complete-task --project "Budget App" --title "Design the database"
python3 main.py list-users
python3 main.py list-projects
python3 main.py list-projects --user "Faith"
python3 main.py search-projects --keyword "budget"
python3 main.py list-tasks --project "Budget App"
```

Add `--help` to see the options, for example `python3 main.py add-task --help`.

### Example output

`python3 main.py list-projects`

```
                                  Projects
┏━━━━┳━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ ID ┃ Title      ┃ Owner ┃ Due        ┃ Progress ┃ Description            ┃
┡━━━━╇━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━┩
│ 1  │ Budget App │ Faith │ 2026-12-31 │ 1/1 done │ Track monthly spending │
└────┴────────────┴───────┴────────────┴──────────┴────────────────────────┘
```

`python3 main.py list-tasks --project "Budget App"`

```
                Tasks in 'Budget App'
┏━━━━┳━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━┓
┃ ID ┃ Title               ┃ Status   ┃ Assigned to ┃
┡━━━━╇━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━┩
│ 1  │ Design the database │ complete │ Faith       │
└────┴─────────────────────┴──────────┴─────────────┘
```

If something is wrong the program shows a message, for example `Error: User 'Faith' not found.`

## Project Structure

```
main.py            CLI entry point (argparse)
models/            classes: Person, User, Project, Task, Tracker
utils/             saving/loading the file, dates, printing tables
data/data.json     where the data is saved
tests/             pytest tests
requirements.txt   packages needed
```

## How It Works

- `User` inherits from `Person`.
- A user has a list of projects and a project has a list of tasks.
- Properties and setters check the data, for example a name cannot be empty.
- Data is saved to `data/data.json` and loaded again when the program starts.
- If the file is missing it starts empty. If it is broken the program shows an error.

## Testing

Run the tests with:

```
pytest
```

## Support

If you find a bug or have a question, open an issue on the GitHub repo:
https://github.com/codewithfaith13/summative-lab-project-tracker/issues

## Roadmap

- Delete and edit users, projects and tasks
- Filter tasks by status
- Show overdue projects

## Known Issues

- You cannot delete or edit users, projects or tasks yet.
- Names and titles must be unique.
- If `data/data.json` is corrupted, you have to fix or delete it.

## Contributing

This is a school project, but suggestions are welcome. To suggest a change, fork the repo, make your change on a new branch, run `pytest` to check the tests pass, and open a pull request.

## Authors

Faith Cherotich ([codewithfaith13](https://github.com/codewithfaith13))

## License

This project was made for learning at Moringa School and has no license.

## Project Status

Finished for the lab. I may add the roadmap features later.
