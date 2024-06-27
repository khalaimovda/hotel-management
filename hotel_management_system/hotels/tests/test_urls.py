from http import HTTPStatus

from django.core.cache import cache
from django.shortcuts import reverse
from django.test import Client, TestCase

from hotels.models import City, Hotel


class URLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.city = City.objects.create(code='CITY', name='City Name')
        cls.hotel = Hotel.objects.create(code='HOTEL', name='Hotel Name', city=cls.city)

        cls.url_template_map = {
            reverse('cities'): 'hotels/cities.html',
            reverse('hotels', kwargs={'city_code': cls.city.code}): 'hotels/hotels.html',
        }

        cls.url_redirect_map = {
            reverse('index'): reverse('cities'),
        }

    def setUp(self):
        cache.clear()
        self.client = Client()

    def test_urls_uses_correct_template(self):
        """The URL uses the appropriate template."""
        for (url, template) in self.url_template_map.items():
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)
                self.assertTemplateUsed(response, template)

    def test_url_redirect(self):
        """Redirection for the root page."""
        for url, redirect_url in self.url_redirect_map.items():
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)

    def test_incorrect_url_response_404(self):
        """Incorrect url with NOT_FOUND status."""
        url = '/some_incorrect_url/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
