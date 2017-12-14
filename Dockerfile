FROM python:3.5-slim
ENV PYTHONUNBUFFERED 1
RUN mkdir /source
WORKDIR /source
ADD requirements.txt /source/
RUN pip install -r requirements.txt
ADD . /source/
EXPOSE 8000
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]