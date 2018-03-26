FROM python:3

RUN pip install Scrapy shub

RUN mkdir /opt/scraper
WORKDIR /opt/scraper

CMD [ "bash" ]
