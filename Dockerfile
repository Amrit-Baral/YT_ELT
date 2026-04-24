# Use the stable Python version you just installed on your Mac
FROM python:3.14-slim

# Create a folder inside the container to hold your code
WORKDIR /app

# Copy the main.py from your Mac into that /app folder
COPY main.py .

# Run the script when the container starts
CMD ["python", "main.py"]