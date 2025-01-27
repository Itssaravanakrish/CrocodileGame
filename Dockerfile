FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python -c "from telegram.ext import Application; Application.initialize(token='6012432098:AAHpJ-7yR7ZmlfCOhKRP-hEk6jqR0hYGsEQ')"

CMD ["python", "main.py"]
