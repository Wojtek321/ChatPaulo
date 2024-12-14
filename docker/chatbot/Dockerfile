FROM python:3.12-alpine

WORKDIR /app

COPY /chatbot/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY /chatbot/ /app/

EXPOSE 7860
ENV GRADIO_SERVER_NAME="0.0.0.0"

ENTRYPOINT ["python", "inference.py"]
