FROM python:3.12
EXPOSE 8000

# Configure Poetry
ENV POETRY_VERSION=1.7.1
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

# Install poetry separated from system interpreter
RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

# Add `poetry` to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"

WORKDIR /sozi_adm

# COPY poetry.lock pyproject.toml ./
COPY . .

RUN poetry install

CMD ["poetry", "run", "python", "manage.py", "makemigrations"]
CMD ["poetry", "run", "python", "manage.py", "migrate"]
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "sozi_adm.wsgi"]