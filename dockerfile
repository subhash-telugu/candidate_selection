FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for building and curl (for uv)
RUN apt-get update -y && apt-get install -y curl build-essential

# Install uv via shell script
RUN curl -Ls https://astral.sh/uv/install.sh | bash
ENV PATH="/root/.cargo/bin:$PATH"

# Copy project files
COPY . /app

# Install Python dependencies using uv
RUN uv lock && uv sync

# Expose port (adjust if needed)
EXPOSE 8001

# Start the app (adjust if using uvicorn/FastAPI)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8001"]

