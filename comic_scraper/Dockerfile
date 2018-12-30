# Use an official Python runtime as a parent image
FROM python:3

RUN mkdir /project

ENV PYTHONUNBUFFERED 1

# Copy the current directory contents into the container at /app
RUN apt-get update && apt-get install -y gcc

# Install any needed packages specified in requirements.txt
COPY ./comic_scraper /project/comic_scraper
COPY . /project
WORKDIR /project/comic_scraper
RUN pip install --trusted-host pypi.python.org -r requirements.txt

CMD ["scrapyd"]


