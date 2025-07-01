FROM python:3.11-slim

WORKDIR /app

COPY . /app


RUN uv lock && uv sync


EXPOSE 8069

CMD ["python", 'app.py']

