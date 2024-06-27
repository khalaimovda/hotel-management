start:
	docker-compose up -d

stop:
	docker-compose down

load_data:
	docker exec -it hotel-management python manage.py loaddata city_hotels.json

create_superuser:
	docker exec -it hotel-management python manage.py createsuperuser
