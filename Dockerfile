FROM python:3.6.7

ENV LANG=C.UTF-8

COPY requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt

COPY . /app
WORKDIR /app

EXPOSE 8088

CMD python worker.py


