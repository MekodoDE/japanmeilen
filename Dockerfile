FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Run app.py when the container launches
CMD ["python", "app.py"]
