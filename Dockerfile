FROM python:3.11-slim-bullseye

RUN apt-get update -y \
    && apt-get upgrade -y \
    && apt-get install python3 build-essential -y

WORKDIR /usr/src/app

COPY pyproject.toml ./

# Install Poetry and project dependencies
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --only main

COPY . .

CMD ["bash","./start.sh"]