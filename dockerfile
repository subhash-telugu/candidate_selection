FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install uv

RUN uv pip compile
RUN uv pip sync

EXPOSE 8001

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8001"]
