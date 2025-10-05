FROM python:3.13-slim

# Ensure stdout/stderr are unbuffered (good for logs)
ENV PYTHONUNBUFFERED=1

# Working directory
WORKDIR /app

# Copy and install Python dependencies via pip
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy application code
COPY main.py /app/main.py

# Default command
CMD ["python", "main.py"]
