# Use a lightweight Python base image
FROM python:3.11-slim

RUN useradd --create-home --shell /bin/bash app_user

# Set working directory
WORKDIR /home/app_user

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
USER app_user

COPY . .

# Set environment variable for MongoDB connection string
ENV MONGODB_URI="mongodb+srv://rhanmif:Ciao1234@urlshortener.vgvnelz.mongodb.net/?retryWrites=true&w=majority&appName=UrlShortener"

# start bash inside docker container
CMD ["bash"]
