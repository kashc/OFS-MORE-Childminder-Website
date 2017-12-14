FROM python:3.5-slim
ENV PYTHONUNBUFFERED 1
RUN mkdir /source
WORKDIR /source
ADD . /source/
RUN pip install -r requirements.txt
EXPOSE 8000
COPY docker-entrypoint.sh /usr/local/bin/
RUN ln -s usr/local/bin/docker-entrypoint.sh / # backwards compat
ENTRYPOINT ["docker-entrypoint.sh"]