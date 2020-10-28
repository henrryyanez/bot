FROM python:3.7

RUN pip install --upgrade pip \
    && mkdir /app

ADD . /app

WORKDIR /app

RUN pip install -r requirements.txt

CMD python /app/bot.py