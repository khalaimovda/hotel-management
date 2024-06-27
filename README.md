# Hotel Management

## Description

- This project implements the test assignment "Integrating third parties" from the company "Maykin Media"
- The project is a Django application with two main pages for displaying Cities and Hotels for each city
- The project includes automatic data loading via HTTP from an external resource using Django Crontab (executing once a day)
- The project features a configured Django Admin Panel, allowing manual editing of database objects
- The project includes Django unit tests that verify the main functionality of the application
- [Poetry](https://python-poetry.org) is used as the dependency manager
- PostgreSQL is used as the database server
- NGING is used as the server
- The project can be run both in development mode using `python manage.py` commands, and in "production" mode using Docker and Docker Compose
- The built application image is hosted on [DockerHub](khalaimovda/hotel-management:0.1.0)

## TL;DR

- Clone GitHub repository
```shell
git clone https://github.com/khalaimovda/hotel-management.git
```

- Start application (docker)
```shell
make start
```

- Load test data
```shell
make load_data
```

- Create superuser
```shell
make create_superuser
```

- Stop application
```shell
make stop
```

- CronJob logs will be available in the `compose-volumes/logs/logfile.log` file

- Main page:`http://127.0.0.1/`

- Admin panel: `http://127.0.0.1/admin/`


## Get Started (Dev)

- Clone GitHub repository
```shell
git clone https://github.com/khalaimovda/hotel-management.git
```

- Activate virtual environment using poetry
```shell
poetry shell
```

- Install dependencies
```shell
poetry install
```

- Run PostgreSQL database
```shell
docker-compose up -d db
```

- Go to main Django application directory
```shell
cd hotel_management_system/
```

- Apply migrations
```shell
python manage.py migrate
```

- Load test data
```shell
python manage.py loaddata city_hotels.json
```

- Create superuser
```shell
python manage.py createsuperuser
```

- Start fetch data cronjob
```shell
python manage.py crontab add
```

- Stop fetch data cronjob
```shell
python manage.py crontab remove
```

- Run test server
```shell
python manage.py runserver
```

- CronJob logs will be available in the `hotel_management_system/logs/logfile.log` file

- Environment variables are set in the `hotel_management_system/.env` file

- Main page:`http://127.0.0.1:8000/`

- Admin panel: `http://127.0.0.1:8000/admin/`
