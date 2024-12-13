FROM python:3.12-alpine

WORKDIR /python-app

COPY /qdrant_db/requirements.txt /python-app/
RUN pip install --no-cache-dir -r requirements.txt

COPY /qdrant_db/ /python-app/

CMD ["python", "load_data.py"]
