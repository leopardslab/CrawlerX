FROM python:3.6-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
RUN pip install --upgrade pip
COPY requirements.txt /code/

RUN pip install -r requirements.txt
COPY . /code/

EXPOSE 8000

CMD ["python3", "manage.py", "migrate"]
CMD ["python3", "manage.py", "createsuperuserwithpassword", "--username ${DJANGO_ADMIN_USERNAME} --password ${DJANGO_ADMIN_PASSWORD} --email ${DJANGO_ADMIN_EMAIL} --preserve"]
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
