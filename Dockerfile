# syntax=docker/dockerfile:1

FROM python:3.11

WORKDIR code

COPY src/backend/requirements.txt /code/requirements.txt
COPY .dockerignore /code/.dockerignore

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY src/backend /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
