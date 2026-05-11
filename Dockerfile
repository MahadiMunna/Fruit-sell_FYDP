FROM python:3.7

ENV PYTHONDONTWRITEBYTECODE=1
 
# Create the app directory
RUN mkdir /app
 
# Set the working directory inside the container
WORKDIR /app

ADD . /app
 
COPY ./requirements.txt  /app/requirements.txt

# run this command to install all dependencies 
RUN pip install -r requirements.txt
 
# Copy the Django project to the container
COPY . /app/