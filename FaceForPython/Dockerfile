FROM python:3.7

RUN mkdir /app
COPY . /app/.
RUN pip install -r /app/requirements.txt -i https://pypi.douban.com/simple
WORKDIR /app

ENV APP_ENV prod

CMD ["python","manager.py"]