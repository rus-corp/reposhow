FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /api

COPY api/requirements.txt ./requirements.txt

RUN pip install --upgrade pip && pip install -r requirements.txt && mkdir -p /code/

COPY api /code/


