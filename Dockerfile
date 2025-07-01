FROM python:3.11-slim

WORKDIR /app

# Copy pyproject.toml (and uv.lock if you have it) for better caching
COPY pyproject.toml /app/
COPY uv.lock /app/  

# Install uv
RUN pip install uv

# Install dependencies
RUN uv pip install --system .

# Copy the rest of the application
COPY . /app

EXPOSE 8001

# Remove --reload for production, it's meant for development
CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8001"]
