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
