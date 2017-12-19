FROM python:3.5-slim
ENV PYTHONUNBUFFERED 1
RUN mkdir /source
WORKDIR /source
ADD . /source/
RUN pip install -r requirements.txt
RUN chmod +x /source/docker-entrypoint.sh
EXPOSE 8000
RUN ["sh /source/docker-entrypoint.sh"]