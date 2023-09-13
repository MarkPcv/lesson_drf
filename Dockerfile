FROM python:3

WORKDIR /code/courses

COPY requirements.txt /code

RUN pip install -r /code/requirements.txt

COPY . .

