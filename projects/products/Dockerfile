# FROM python:3.12-slim-bookworm

# WORKDIR /app

# COPY . .

# RUN pip install poetry
# RUN poetry install --without dev

# EXPOSE 8000

# ENTRYPOINT ["poetry", "run"]
# CMD ["uvicorn", "app.main:app", "--host 0.0.0.0"]

FROM python:3.12-slim-bookworm

WORKDIR /app

RUN pip install poetry

COPY . .
RUN poetry install

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host=0.0.0.0", "--port=8000"]

