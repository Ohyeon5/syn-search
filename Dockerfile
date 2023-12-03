# syntax=docker/dockerfile:1

FROM python:3.11

WORKDIR code

COPY src/backend/requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY src .
ENV PYTHONPATH "./src"
COPY gunicorn.conf.py .
COPY .dockerignore .

EXPOSE 3100

CMD ["gunicorn", "backend.main:app"]
