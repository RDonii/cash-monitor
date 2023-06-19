FROM python:3.10.11
WORKDIR '/app'

RUN pip3 install gunicorn
COPY ./requirements.txt /app
RUN pip3 install -r requirements.txt
EXPOSE 8080
COPY . /app
RUN ["chmod", "-R", "777", "/app/deploy"]