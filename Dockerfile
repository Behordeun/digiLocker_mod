# Use the official Python base image
FROM python:3.9.18

# Set the arguments
ARG APP_SECRETKEY
ARG DROPBOX_KEY
ARG DROPBOX_SECRET
ARG DROPBOX_ACCESS_TYPE
ARG DROPBOX_ACCESS_TOKEN
ARG MAIL_USERNAME
ARG MAIL_PASSWORD
ARG MAIL_DEFAULT_SENDER
ARG MAIL_SENDER
ARG SECRET_KEY
ARG SERVER_BASE_ADDRESS
ARG SEPOLIA_URL
ARG PRIVATE_KEY
ARG DAPR_PORT
ARG DAPR_GRPC_PORT
ARG DAPR_HTTP_PORT
ARG DAPR_APP_PORT

# Set the environment variables
ENV APP_SECRETKEY=$APP_SECRETKEY
ENV DROPBOX_KEY=$DROPBOX_KEY
ENV DROPBOX_SECRET=$DROPBOX_SECRET
ENV DROPBOX_ACCESS_TYPE=$DROPBOX_ACCESS_TYPE
ENV DROPBOX_ACCESS_TOKEN=$DROPBOX_ACCESS_TOKEN
ENV MAIL_USERNAME=$MAIL_USERNAME
ENV MAIL_PASSWORD=$MAIL_PASSWORD
ENV MAIL_DEFAULT_SENDER=$MAIL_DEFAULT_SENDER
ENV MAIL_SENDER=$MAIL_SENDER
ENV SECRET_KEY=$SECRET_KEY
ENV SERVER_BASE_ADDRESS=$SERVER_BASE_ADDRESS
ENV SEPOLIA_URL=$SEPOLIA_URL
ENV PRIVATE_KEY=$PRIVATE_KEY
ENV DAPR_PORT=3500
ENV DAPR_GRPC_PORT=50001
ENV DAPR_HTTP_PORT=3501
ENV DAPR_APP_PORT=8083

COPY requirements.txt /app/requirements.txt

# Create a directory for your app and set it as the working directory
WORKDIR /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache -r requirements.txt

# Expose the ports your app runs on
EXPOSE $DAPR_APP_PORT

# Copy the current directory contents into the container at /app
COPY . /app/

# Set the entry point for the application to Python
ENTRYPOINT [ "python" ]

HEALTHCHECK --interval=5s --timeout=3s CMD curl -f http://localhost:8083 || nc -zv localhost 8083 || exit 1

# Run main.py when the container launches
CMD ["main.py"]