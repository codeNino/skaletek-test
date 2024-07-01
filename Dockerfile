# Use the official Python image as base
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install pipenv
RUN pip install --no-cache-dir pipenv

# Install dependencies using pipenv
RUN pipenv install --system --deploy

# Define the command to run your application
CMD ["python", "main.py"]
