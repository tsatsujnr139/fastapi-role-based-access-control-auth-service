#!/bin/bash
set -e

#Wait for db to start
python /app/app/tests_pre_start.py

# Run migrations
alembic upgrade head

# Create initial data in DB
python /app/app/initial_test_data.py

# Run tests
pytest --cov=app --cov-report=term-missing tests