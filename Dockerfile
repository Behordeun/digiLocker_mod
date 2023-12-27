# Use the official Python base image
FROM python:3.9.18


COPY requirements.txt /app/requirements.txt

# Create a directory for your app and set it as the working directory
WORKDIR /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache -r requirements.txt

# Expose the ports your app runs on
EXPOSE 8083

# Copy the current directory contents into the container at /app
COPY . /app/

# Set the entry point for the application to Python
ENTRYPOINT [ "python" ]

HEALTHCHECK --interval=5s --timeout=3s CMD curl -f http://localhost:8083 || nc -zv localhost 8083 || exit 1

# Run main.py when the container launches
CMD ["main.py"]