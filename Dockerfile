FROM python:3.11-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Add to PATH
ENV PATH="/root/.local/bin:$PATH"

# Install project dependencies
COPY pyproject.toml uv.lock /app/
RUN uv pip install --system .

# Copy app code
COPY . /app

EXPOSE 8001

CMD ["uvicorn", "src.candidate_selection.web.app:app", "--host", "0.0.0.0", "--port", "8001"]
