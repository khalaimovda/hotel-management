import uuid

from django.db import connections
from django.db.models import ObjectDoesNotExist
from django.db.utils import IntegrityError
from django.test import TestCase

from hotels.models import City, Hotel


class CityModelTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.city = City.objects.create(code='CITY', name='City Name')

    def test_model_creation(self):
        self.assertIsInstance(self.city.id, uuid.UUID)
        self.assertEqual(self.city.code, 'CITY')
        self.assertEqual(self.city.name, 'City Name')

    def test_code_unique_constraint(self):
        City.objects.create(code='UNIQUE', name='City Name Unique 1')
        with self.assertRaises(IntegrityError):
            City.objects.create(code='UNIQUE', name='City Name Unique 2')

    def test_str(self):
        """__str__ in the model matches the name field"""
        self.assertEqual(self.city.__str__(), 'City Name')


class HotelModelTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.city = City.objects.create(code='CITY', name='City Name')
        cls.hotel = Hotel.objects.create(code='HOTEL', name='Hotel Name', city=cls.city)

    def test_model_creation(self):
        self.assertIsInstance(self.hotel.id, uuid.UUID)
        self.assertEqual(self.hotel.code, 'HOTEL')
        self.assertEqual(self.hotel.name, 'Hotel Name')
        self.assertEqual(self.hotel.city, self.city)

    def test_foreign_key_constraint(self):
        with self.assertRaises(IntegrityError):
            Hotel.objects.create(code='HOTEL2', name='Hotel Name 2', city_id=uuid.uuid4())
            connections['default'].check_constraints()  # This line is needed to catch the exception

    def test_code_unique_constraint(self):
        Hotel.objects.create(code='UNIQUE', name='Hotel Name Unique 1', city=self.city)
        with self.assertRaises(IntegrityError):
            Hotel.objects.create(code='UNIQUE', name='Hotel Name Unique 2', city=self.city)

    def test_foreign_key_deletion(self):
        city = City.objects.create(code='CITYDEL', name='City to delete')
        Hotel.objects.create(code='HOTELDEL', name='Hotel to delete', city=city)
        city.delete()
        with self.assertRaises(ObjectDoesNotExist):
            Hotel.objects.get(code='HOTELDEL')

    def test_str(self):
        """__str__ in the model matches the name field"""
        self.assertEqual(self.hotel.__str__(), 'Hotel Name')
