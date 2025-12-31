# Use the official Python runtime image
FROM python:3.12-slim

# Set environment variables 
# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
#Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1 

# Create the app directory
RUN mkdir /app
 
# Set the working directory inside the container
WORKDIR /app

# Copy the Django project  and install dependencies
COPY requirements.txt  /app/

# Upgrade pip
RUN pip3 install --upgrade pip 
 
# run this command to install all dependencies 
RUN pip3 install -r requirements.txt

# Copy the Django project to the container
COPY ./core /app
 
# Expose the Django port
EXPOSE 8000
 
# Run Django’s development server
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]