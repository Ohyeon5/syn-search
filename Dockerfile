# syntax=docker/dockerfile:1

FROM python:3.11

WORKDIR /code

COPY src/backend/requirements.txt /code/requirements.txt
COPY .dockerignore /code/.dockerignore

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY src/preprocessing /code/preprocessing
RUN pip install --no-cache-dir --upgrade -e /code/preprocessing

COPY src/backend /code/app
COPY data/index/I20160920.index /code/llama-index

ENV PORT=3100
EXPOSE 3100

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3100"]
