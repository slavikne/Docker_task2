FROM python:3.9-alpine
WORKDIR /DJ_CRUD_stocks-main
COPY . .
RUN pip install -r /DJ_CRUD_stocks-main/requirements.txt
CMD ["python", "/DJ_CRUD_stocks-main/manage.py", "runserver", "0.0.0.0:8000"]