import csv
import io
import logging
from collections import defaultdict

import requests
from django.db import transaction, DatabaseError
from requests.auth import HTTPBasicAuth

from .models import City, Hotel

logger = logging.getLogger(__name__)


def fetch_csv_data(url: str, username: str, password: str) -> list[list[str]]:
    response: requests.models.Response = requests.get(url, auth=HTTPBasicAuth(username=username, password=password))
    csv_content = response.content.decode('utf-8')
    csv_file = io.StringIO(csv_content)
    csv_reader = csv.reader(csv_file, delimiter=';')
    return list(csv_reader)


def fetch_hotel_data(city_url: str, hotel_url: str, username: str, password: str):
    """
    Fetches CSV files with cities and hotels using authenticated HTTP and loads them into the database

    The first revision: clear all previous data and load the new one
    This approach has some conflicts with management system.
    I plan to discuss alternative solutions during the interview.
    """
    logger.info('Data fetch cronjob started')

    try:
        # [['AMS', 'Amsterdam'], ['ANT', 'Antwerpen'], ... ]
        city_list = fetch_csv_data(url=city_url, username=username, password=password)

        # [['AMS', 'AMS01', 'Ibis'], ['AMS', 'AMS02', 'Novotel'], ... ]
        hotel_list = fetch_csv_data(url=hotel_url, username=username, password=password)

        # {'AMS': 'Amsterdam', 'ANT': 'Antwerpen', ... }
        city_dict: dict[str, str] = {c[0]: c[1] for c in city_list}

        # {'AMS': [('AMS01', 'Ibis'), ('AMS02', 'Novotel'), ... ], 'ANT': [(...), (...), ... ], ... }
        hotel_dict: dict[str, list] = defaultdict(list)
        for h in hotel_list:
            hotel_dict[h[0]].append((h[1], h[2]))
    except Exception:
        logger.error('Data fetch cronjob parsing error', exc_info=True)
        return

    try:
        with transaction.atomic():
            # Clear all data (Impossible to execute "truncate" without raw sql)
            City.objects.all().delete()

            # Prepare models
            cities: list[City] = []
            hotels: list[Hotel] = []
            for city_code, city_name in city_dict.items():
                city = City(code=city_code, name=city_name)
                cities.append(city)
                for hotel_code, hotel_name in hotel_dict[city_code]:
                    hotel = Hotel(code=hotel_code, name=hotel_name, city=city)
                    hotels.append(hotel)

            # Create all new models
            City.objects.bulk_create(cities)
            Hotel.objects.bulk_create(hotels)
    except DatabaseError:
        logger.error('Data fetch cronjob transaction rollback', exc_info=True)
        return

    logger.info('New data (cronjob) uploaded successfully')
