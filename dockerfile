FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN apt-get update -y && apt-get install -y curl build-essential

# Install uv and move it to a global path
RUN curl -Ls https://astral.sh/uv/install.sh | bash && \
    mv /root/.cargo/bin/uv /usr/local/bin/uv

# Copy project files
COPY . /app

# Install Python dependencies
RUN uv lock && uv sync

EXPOSE 8001

CMD ["python", "app.py"]
