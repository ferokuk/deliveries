FROM python:3.12-slim-bullseye
LABEL authors="Yaroslav"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /deliveries/backend/

COPY requirements.txt ./

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "deliveries_test_task.wsgi:application", "--bind", "0.0.0.0:8000"]


