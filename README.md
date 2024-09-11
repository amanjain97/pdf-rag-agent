# pdf-rag-agent

The project is built using an MVC (Model-View-Controller) architecture and follows Flask best practices, including error handling and validation using Pydantic.

## Project Structure

```bash
pdf-rag-agent/
│
├── app.py                    # Main Flask app entry point
├── controllers/
│   └── pdf_controller.py      # Controller for handling logic of upload and ask endpoints
├── models/
│   └── pdf_model.py    # Pydantic models for request 
├── utils/
│   └── file_utils.py          # Utility functions for checking file paths
├── config/
│   └── config.py          # Env variable and configuration constants
├── templates/
│   └── template.py          # Prompts and templates
├── Pipfile                    # Pipenv dependencies
└── Pipfile.lock               # Lockfile for dependencies
```

## Prerequisites

Make sure you have the following installed on your machine:

- Python 3.11+
- Pipenv for managing virtual environments and dependencies.

To install Pipenv, run:
```
pip install pipenv
```

## Installation
1. Activate the virtual environment:
```
pipenv shell
```

2. Install dependencies using Pipenv:
```
pipenv install
```
## Running the Server
Run the Flask server:
```
pipenv run python app.py
```
By default, the server will run at http://127.0.0.1:8000
