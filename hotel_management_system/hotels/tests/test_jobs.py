from collections import defaultdict
from unittest.mock import patch, Mock

from django.test import TestCase
from requests.auth import HTTPBasicAuth

from hotels.jobs import fetch_hotel_data
from hotels.models import City, Hotel


class FetchHotelDataTest(TestCase):

    @patch('hotels.jobs.requests.get')
    def test_load_csv_to_db(self, mock_requests_get):

        # Create some previous data (out job has to clear them)
        cities_prev = [City(code='CITY1', name='City Name 1'), City(code='CITY2', name='City Name 2')]
        hotels_prev = [
            Hotel(code='CITY1H1', name='Hotel Name 11', city=cities_prev[0]),
            Hotel(code='CITY1H2', name='Hotel Name 12', city=cities_prev[0]),
            Hotel(code='CITY2H1', name='Hotel Name 21', city=cities_prev[1]),
            Hotel(code='CITY2H2', name='Hotel Name 22', city=cities_prev[1]),
        ]
        City.objects.bulk_create(cities_prev)
        Hotel.objects.bulk_create(hotels_prev)

        # Mock requests.get
        csv_city_content = '"AMS";"Amsterdam"\n"ANT";"Antwerpen"\n"BAR";"Barcelona"'
        csv_hotel_content = (
            '"AMS";"AMS01";"Ibis Amsterdam Airport"\n"AMS";"AMS02";"Novotel Amsterdam Airport"\n'
            '"ANT";"ANT01";"Express by Holiday Inn"\n"ANT";"ANT02";"Eden"\n"ANT";"ANT04";"Astoria"\n'
            '"BAR";"BARA1";"Nouvel"\n"BAR";"BARA2";"Lleo"\n"BAR";"BARA6";"H10 Universitat"'
        )

        correct_relations = {
            'AMS': (
                'Amsterdam',
                {
                    ('AMS01', 'Ibis Amsterdam Airport'), ('AMS02', 'Novotel Amsterdam Airport')
                }
            ),
            'ANT': (
                'Antwerpen',
                {
                    ('ANT01', 'Express by Holiday Inn'), ('ANT02', 'Eden'), ('ANT04', 'Astoria')
                }
            ),
            'BAR': (
                'Barcelona',
                {
                    ('BARA1', 'Nouvel'), ('BARA2', 'Lleo'), ('BARA6', 'H10 Universitat')
                }
            )
        }

        mock_response_city = Mock()
        mock_response_city.status_code = 200
        mock_response_city.content = csv_city_content.encode('utf-8')

        mock_response_hotel = Mock()
        mock_response_hotel.status_code = 200
        mock_response_hotel.content = csv_hotel_content.encode('utf-8')

        city_url = 'http://example.com/city.csv'
        hotel_url = 'http://example.com/hotel.csv'
        username = 'username'
        password = 'password'

        def side_effect(url, auth=None):
            if url == city_url:
                return mock_response_city
            elif url == hotel_url:
                return mock_response_hotel
            else:
                raise ValueError('Unmocked URL: ' + url)

        mock_requests_get.side_effect = side_effect

        # Execute our job
        fetch_hotel_data(city_url=city_url, hotel_url=hotel_url, username=username, password=password)

        # Verify database models
        cities = City.objects.all()
        hotels = Hotel.objects.all()
        self.assertEqual(len(cities), 3)
        self.assertEqual(len(hotels), 8)

        actual_relations = dict()
        city_dict: dict[str, str] = {c.code: c.name for c in cities}
        hotel_dict: dict[str, list] = defaultdict(list)
        for h in hotels:
            hotel_dict[h.city.code].append((h.code, h.name))
        self.assertEqual(city_dict.keys(), hotel_dict.keys())
        for city_code in city_dict:
            actual_relations[city_code] = (
                city_dict[city_code],
                set(hotel_dict[city_code])
            )

        self.assertEqual(actual_relations, correct_relations)

        # Verify that requests.get was called with the correct URLs
        mock_requests_get.assert_any_call(city_url, auth=HTTPBasicAuth(username, password))
        mock_requests_get.assert_any_call(hotel_url, auth=HTTPBasicAuth(username, password))
        self.assertEqual(mock_requests_get.call_count, 2)
