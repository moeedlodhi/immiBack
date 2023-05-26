FROM python:3.9-alpine3.13
LABEL maintainer="moeed"

ENV PYTHONUNBUFFERED 1

COPY ./backend /backend
COPY ./requirements.txt /backend/requirements.txt
WORKDIR /backend

RUN python -m venv new_env
RUN source new_env/bin/activate
RUN pip install -r requirements.txt




