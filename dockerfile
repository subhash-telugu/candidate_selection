FROM python:3.11-slim

WORKDIR /app

COPY . /app


RUN uv lock && uv sync


EXPOSE 8001

CMD ["python", "app.py"]

