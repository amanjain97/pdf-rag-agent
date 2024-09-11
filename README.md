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

## Output

#### Upload the file

```
$ curl --location 'localhost:8000/v1/upload' \
--header 'Content-Type: application/json' \
--data '{
    "file_path":"handbook.pdf"
}'

{"filename":"handbook.pdf","status":"success"}
```

#### Ask the questions

```
curl --location 'http://localhost:8000/v1/ask' \
--header 'Content-Type: application/json' \
--data '{
    "questions": ["Who is the CEO of the company?", "What is the name of the company?", "What is their vacation policy?", "What is the annual revenue growth of the company?"]
}'
```

Output

```
{"What is the annual revenue growth of the company?":"Data Not Available","What is the name of the company?":"Zania Inc.","What is their vacation policy?":"The vacation policy includes the following key points:\n\n1. Vacation granted during the first year of employment is prorated based on the hire date.\n2. Eligible employees accrue a certain amount of vacation for every period of time worked, up to a maximum accrual limit.\n3. Once the maximum accrual is reached, no additional vacation will accrue until some of the unused vacation is taken.\n4. Employees are encouraged to use their vacation time, which can be used immediately upon hire or after a certain period.\n5. Vacation requests should be made in advance, and the company generally grants requests considering business needs.\n6. Vacation must be taken in specified increments.\n7. Unused vacation may be required to be used during certain leaves of absence.\n8. Carryover of unused vacation can vary; it may be carried over to the following year or forfeited depending on company policy.\n9. Upon separation from employment, earned but unused vacation may be forfeited or paid out depending on state law.\n\nOverall, the policy emphasizes the accrual and usage of vacation time while considering business needs and legal regulations.","Who is the CEO of the company?":"Shruti Gupta"}
```

## Further steps

1. Use gaurdrails.ai to gaurdrail the application.
2. Perform evalaution for the LLM App.
3. Add slack notification integration.
4. Make application faster using threading to get answer to each question.
