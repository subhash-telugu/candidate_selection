FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install uv

RUN uv pip compile
RUN uv pip sync

EXPOSE 8001

CMD ["python", "app.py"]