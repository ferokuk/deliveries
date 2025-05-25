FROM python:3.12-slim-bullseye
LABEL authors="Yaroslav"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /deliveries/backend/

COPY requirements.txt /deliveries/backend/

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . /deliveries/backend/

COPY entrypoint.sh /deliveries/backend/entrypoint.sh
RUN chmod +x /deliveries/backend/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/deliveries/backend/entrypoint.sh"]
