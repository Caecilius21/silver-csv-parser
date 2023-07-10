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
Get-ChildItem -Path . -Recurse -Filter \*.pyc | Remove-Item -Force
