
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app/

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./pyproject.toml ./poetry.lock* /app/

ARG ENVIRONMENT=test
RUN bash -c "if [ $ENVIRONMENT == "dev" ] || [ $ENVIRONMENT == "prod" ] ; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"

COPY . /app/

COPY ./startup.sh /app/

COPY ./test.sh /app/

RUN chmod +x /app/startup.sh

RUN chmod +x /app/test.sh
