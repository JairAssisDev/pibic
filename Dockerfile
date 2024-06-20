FROM python:3.11

WORKDIR /app

COPY . .

RUN curl https://pyenv.run | bash

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --only main

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "--timeout", "6000", "main:app"]
