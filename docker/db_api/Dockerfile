FROM python:3.12-alpine

WORKDIR /app

COPY /db_api/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY /db_api/ /app/

EXPOSE 8000

ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]
