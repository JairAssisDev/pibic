FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install gunicorn

RUN pip install poetry

RUN poetry config virtualenvs.create false && poetry install --no-dev

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "run:app"]

