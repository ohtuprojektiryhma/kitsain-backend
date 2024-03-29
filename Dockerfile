FROM python:3.10-alpine

WORKDIR /app

COPY . ./

RUN chgrp -R 0 /app && \
    chmod -R g=u /app

RUN pip install poetry

ENV POETRY_VIRTUALENVS_IN_PROJECT=true

EXPOSE 5000

RUN poetry config installer.max-workers 10

RUN poetry install --no-root

ENTRYPOINT ["poetry", "run", "flask", "--app", "src/app.py", "run", "--host", "0.0.0.0"]