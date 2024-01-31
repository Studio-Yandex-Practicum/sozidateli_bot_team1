FROM python:3.10-slim as builder

RUN apt-get update && apt-get install -y \
    python3-dev \
    gcc \
    libc-dev \
    libffi-dev \
    libpq-dev

RUN pip install poetry==1.4.1

WORKDIR /app

COPY ./pyproject.toml ./poetry.lock ./

# COPY ./README.md .

RUN mkdir "src" && echo "import this" > src/main.py

RUN poetry install

FROM python:3.10-slim

COPY --from=builder /root/.cache/pypoetry/virtualenvs/ /root/.cache/pypoetry/virtualenvs/

RUN pip install poetry==1.4.1

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY . .

CMD ["poetry", "run", "python", "main.py"]
