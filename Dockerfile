# Use official Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY . .

# Expose port if Flask/FastAPI is used (change if needed)
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
