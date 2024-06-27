from django.conf import settings
from django.shortcuts import reverse
from django.test import Client, TestCase

from hotels.models import City, Hotel


class CityViewTests(TestCase):

    def setUp(self):
        self.url = reverse('cities')
        self.title = 'Cities'
        self.client = Client()

    def test_correct_context_for_single_page_without_search(self):
        city = City.objects.create(code='CITY', name='City Name')
        response = self.client.get(self.url)
        self.assertEqual(response.context['title'], self.title)
        self.assertIsNone(response.context['search'])
        self.assertEqual(len(response.context['cities']), 1)
        self.assertEqual(response.context['cities'][0], city)

    def test_correct_context_for_two_pages_without_search(self):
        cities = [City(code=f'CITY{i}', name=f'City Name {i}') for i in range(settings.ITEMS_PER_PAGE + 1)]
        City.objects.bulk_create(cities)
        cities.sort(key=lambda x: (x.code, x.name))
        first_page = self.client.get(self.url)
        second_page = self.client.get(self.url + '?page=2')

        self.assertEqual(first_page.context['title'], self.title)
        self.assertIsNone(first_page.context['search'])
        self.assertEqual(len(first_page.context['cities']), settings.ITEMS_PER_PAGE)
        # Cities should be ordered by (code, name)
        # I understand that this sorting is by digits (not numbers)
        # This can be adjusted if the code format for hotels is clearly defined
        self.assertEqual(first_page.context['cities'].object_list, cities[:settings.ITEMS_PER_PAGE])

        self.assertEqual(second_page.context['title'], self.title)
        self.assertIsNone(second_page.context['search'])
        self.assertEqual(len(second_page.context['cities']), 1)
        self.assertEqual(second_page.context['cities'][0], cities[-1])

    def test_correct_context_for_single_page_with_search_positive(self):
        search = 'iT'
        city = City.objects.create(code='CITY', name='City Name')
        response = self.client.get(self.url + f'?search={search}')
        self.assertEqual(response.context['title'], self.title)
        self.assertEqual(response.context['search'], search)
        self.assertEqual(len(response.context['cities']), 1)
        self.assertEqual(response.context['cities'][0], city)

    def test_correct_context_for_single_page_with_search_negative(self):
        search = 'Pity'
        City.objects.create(code='CITY', name='City Name')
        response = self.client.get(self.url + f'?search={search}')
        self.assertEqual(response.context['title'], self.title)
        self.assertEqual(response.context['search'], search)
        self.assertEqual(len(response.context['cities']), 0)

    def test_correct_context_for_two_pages_with_search_positive(self):
        search = 'Name 0'
        cities = [City(code=f'CITY{i}', name=f'City Name {i}') for i in range(settings.ITEMS_PER_PAGE + 1)]
        City.objects.bulk_create(cities)
        response = self.client.get(self.url + f'?search={search}')
        self.assertEqual(response.context['title'], self.title)
        self.assertEqual(response.context['search'], search)
        self.assertEqual(len(response.context['cities']), 1)
        self.assertEqual(response.context['cities'][0], cities[0])

        second_page_response = self.client.get(self.url + '?page=2' + '&' + f'search={search}')
        self.assertEqual(second_page_response.context['title'], self.title)
        self.assertEqual(second_page_response.context['search'], search)
        self.assertEqual(len(second_page_response.context['cities']), 1)
        self.assertEqual(second_page_response.context['cities'][0], cities[0])

    def test_correct_context_for_two_pages_with_search_negative(self):
        search = 'Name -1'
        cities = [City(code=f'CITY{i}', name=f'City Name {i}') for i in range(settings.ITEMS_PER_PAGE + 1)]
        City.objects.bulk_create(cities)
        response = self.client.get(self.url + f'?search={search}')
        self.assertEqual(response.context['title'], self.title)
        self.assertEqual(response.context['search'], search)
        self.assertEqual(len(response.context['cities']), 0)

        second_page_response = self.client.get(self.url + '?page=2' + '&' + f'search={search}')
        self.assertEqual(second_page_response.context['title'], self.title)
        self.assertEqual(second_page_response.context['search'], search)
        self.assertEqual(len(second_page_response.context['cities']), 0)


class HotelViewTests(TestCase):

    def setUp(self):
        self.city = City.objects.create(code='CITY', name='City Name')
        self.url = reverse('hotels', kwargs={'city_code': self.city.code})
        self.title = 'Hotels'
        self.client = Client()

    def test_correct_context_for_single_page_without_search(self):
        hotel = Hotel.objects.create(code='HOTEL', name='Hotel Name', city=self.city)
        response = self.client.get(self.url)
        self.assertEqual(response.context['title'], self.title)
        self.assertIsNone(response.context['search'])
        self.assertEqual(len(response.context['hotels']), 1)
        self.assertEqual(response.context['hotels'][0], hotel)

    def test_correct_context_for_two_pages_without_search(self):
        hotels = [
            Hotel(code=f'HOTEL{i}', name=f'Hotel Name {i}', city=self.city)
            for i in range(settings.ITEMS_PER_PAGE + 1)
        ]
        Hotel.objects.bulk_create(hotels)
        hotels.sort(key=lambda x: (x.code, x.name))
        first_page = self.client.get(self.url)
        second_page = self.client.get(self.url + '?page=2')

        self.assertEqual(first_page.context['title'], self.title)
        self.assertIsNone(first_page.context['search'])
        self.assertEqual(len(first_page.context['hotels']), settings.ITEMS_PER_PAGE)
        # Hotels should be ordered by (code, name)
        # I understand that this sorting is by digits (not numbers)
        # This can be adjusted if the code format for hotels is clearly defined
        self.assertEqual(first_page.context['hotels'].object_list, hotels[:settings.ITEMS_PER_PAGE])

        self.assertEqual(second_page.context['title'], self.title)
        self.assertIsNone(second_page.context['search'])
        self.assertEqual(len(second_page.context['hotels']), 1)
        self.assertEqual(second_page.context['hotels'][0], hotels[-1])

    def test_correct_context_for_single_page_with_search_positive(self):
        search = 'oT'
        hotel = Hotel.objects.create(code='HOTEL', name='Hotel Name', city=self.city)
        response = self.client.get(self.url + f'?search={search}')
        self.assertEqual(response.context['title'], self.title)
        self.assertEqual(response.context['search'], search)
        self.assertEqual(len(response.context['hotels']), 1)
        self.assertEqual(response.context['hotels'][0], hotel)

    def test_correct_context_for_single_page_with_search_negative(self):
        search = 'Pity'
        Hotel.objects.create(code='HOTEL', name='Hotel Name', city=self.city)
        response = self.client.get(self.url + f'?search={search}')
        self.assertEqual(response.context['title'], self.title)
        self.assertEqual(response.context['search'], search)
        self.assertEqual(len(response.context['hotels']), 0)

    def test_correct_context_for_two_pages_with_search_positive(self):
        search = 'Name 0'
        hotels = [
            Hotel(code=f'HOTEL{i}', name=f'Hotel Name {i}', city=self.city)
            for i in range(settings.ITEMS_PER_PAGE + 1)
        ]
        Hotel.objects.bulk_create(hotels)
        response = self.client.get(self.url + f'?search={search}')
        self.assertEqual(response.context['title'], self.title)
        self.assertEqual(response.context['search'], search)
        self.assertEqual(len(response.context['hotels']), 1)
        self.assertEqual(response.context['hotels'][0], hotels[0])

        second_page_response = self.client.get(self.url + '?page=2' + '&' + f'search={search}')
        self.assertEqual(second_page_response.context['title'], self.title)
        self.assertEqual(second_page_response.context['search'], search)
        self.assertEqual(len(second_page_response.context['hotels']), 1)
        self.assertEqual(second_page_response.context['hotels'][0], hotels[0])

    def test_correct_context_for_two_pages_with_search_negative(self):
        search = 'Name -1'
        hotels = [
            Hotel(code=f'HOTEL{i}', name=f'Hotel Name {i}', city=self.city)
            for i in range(settings.ITEMS_PER_PAGE + 1)
        ]
        Hotel.objects.bulk_create(hotels)
        response = self.client.get(self.url + f'?search={search}')
        self.assertEqual(response.context['title'], self.title)
        self.assertEqual(response.context['search'], search)
        self.assertEqual(len(response.context['hotels']), 0)

        second_page_response = self.client.get(self.url + '?page=2' + '&' + f'search={search}')
        self.assertEqual(second_page_response.context['title'], self.title)
        self.assertEqual(second_page_response.context['search'], search)
        self.assertEqual(len(second_page_response.context['hotels']), 0)

# I understand that there is quite a lot of duplicate code here
# I am ready to refactor it if necessary for the test assignment
