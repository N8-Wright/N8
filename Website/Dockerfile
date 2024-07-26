FROM python:3.12

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./src /app
COPY ./src/static /static
COPY ./src/templates /templates

# Run the application
CMD ["uvicorn", "website:app", "--app-dir", "app", "--host", "0.0.0.0", "--port", "80"]