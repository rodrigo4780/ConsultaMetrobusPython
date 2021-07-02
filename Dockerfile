FROM python:3.8.6

ADD requirements.txt /app/requirements.txt

RUN python -m venv /env

RUN /env/bin/pip install --upgrade pip

RUN /env/bin/pip install --no-cache-dir -r /app/requirements.txt

COPY ApiMetrobus /app
WORKDIR /app
ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH
ENV HOSTBASE 172.17.0.2
EXPOSE 8080

#CMD ["python", "manage.py", "runserver", "8080"]
CMD ["gunicorn", "--chdir", "ApiMetrobus", "--bind", ":8080", "ApiMetrobus.wsgi:application", "--timeout", "1000", "--graceful-timeout", "100"]