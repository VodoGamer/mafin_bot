FROM python:3.10-slim

ENV TZ Europe/Moscow

ARG PROJECT_NAME
WORKDIR /$PROJECT_NAME

RUN pip install poetry

COPY poetry.loc[k] pyproject.toml README.md ./
RUN poetry install --only main
COPY . ./
CMD [ "poetry", "run", "python", "-m", "src" ]
