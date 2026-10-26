# Thaif AI Production System

A production-style text-processing application built with FastAPI and Streamlit.

[![Python Tests](https://github.com/THAIF74/Thaif-AI-Production-System/actions/workflows/python-tests.yml/badge.svg)](https://github.com/THAIF74/Thaif-AI-Production-System/actions/workflows/python-tests.yml)

## Features

- REST API with request validation
- Health and uptime endpoint
- Structured request logging
- Unique request ID response headers
- Text processing and statistics
- Streamlit user interface
- Automated API tests
- Environment-based API URL configuration

## Run locally

Install dependencies:

    python -m pip install -r requirements.txt

Start the API in terminal 1:

    python -m uvicorn api:app --reload

Start the frontend in terminal 2:

    python -m streamlit run app.py

Open http://127.0.0.1:8000/docs to explore the API.

## Run tests

    python -m pytest -v

## Important

This is a production-style learning project, not a security-audited production service. Text processing is deterministic and does not call an external AI model.
## API Examples

### Check API health

```bash
curl http://127.0.0.1:8000/health
```

### Explore API documentation

Start the API locally, then visit:

http://127.0.0.1:8000/docs

Use the interactive Swagger UI to inspect endpoints, submit requests, and view responses.

### Run automated tests

```bash
python -m pytest -v
```

The tests validate the API behavior and help catch regressions when the project changes.
