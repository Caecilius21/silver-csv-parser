# run server

python manage.py runserver

# rebundle frontend

cd frontend
npm run dev

# run tests

python manage.py test
coverage run --source='.' manage.py test

# run docker

Build the container image.
$ docker build -t csv-parser .
Start your container
$ docker run -dp 127.0.0.1:8000:8000 csv-parser

# generate test report

coverage html
coverage report

# TODO

- docker
- postgresql
