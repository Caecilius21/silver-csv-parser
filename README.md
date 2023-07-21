# CSV Parser application

## run server

python manage.py runserver

## Bundle frontend

cd frontend
npm run dev

## run docker

Build the container image.
$ docker build -t config .
Start your container
$ docker run -p 8000:8000 config

## clear pycache

Get-ChildItem -Path . -Recurse -Filter **pycache** | Remove-Item -Force -Recurse
Get-ChildItem -Path . -Recurse -Filter **.pyc** | Remove-Item -Force

## Possible improvements

create a general context for the app:

- When deleting or adding data to the database, it will automatically refresh the table
- Add a job that automatically fetch data using either lambda functions, or airflow
-
