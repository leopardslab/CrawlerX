# As Scrapy runs on Python, I choose the official Python 3 Docker image.
FROM python:3

# Set the working directory to /usr/src/app.
WORKDIR /usr/src/app

# Copy the file from the local host to the filesystem of the container at the working directory.
COPY requirements.txt ./

# Install Scrapy specified in requirements.txt.
RUN pip3 install --no-cache-dir -r requirements.txt

WORKDIR /usr/src/app
# Copy the project source code from the local host to the filesystem of the container at the working directory.
COPY . /usr/src/app

# Expose web GUI
EXPOSE 6800
EXPOSE 27017
EXPOSE 5672

RUN chmod +x /usr/src/app/deploy.sh
RUN /usr/src/app/deploy.sh

CMD ["scrapyd" ]
