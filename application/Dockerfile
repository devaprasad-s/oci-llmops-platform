FROM python:3.10-slim
WORKDIR /app

# Install the application dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cpu -r requirements.txt

# Copy in the source code
COPY . .

# Setup an app user so the container doesn't run as the root user
RUN useradd -m app && chown -R app:app /app
USER app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]