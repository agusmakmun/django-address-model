# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django_address.models import (Country, Province,
                                   District, SubDistrict)


class TestModels(TestCase):

    def setUp(self):
        country_data = {'name': 'Indonesia', 'states': [], 'code': 'ID',
                        'phone_code': '+62', 'currency_code': 'IDR'}
        province_data = {'name': 'Sumatera Selatan', 'country_id': 1}
        district_data = {'name': 'Ogan Komering Ilir', 'province_id': 1}
        sub_district_data = {'name': 'Sungai Minang', 'district_id': 1,
                             'postal_code': '36455'}

        self.country = Country.objects.create(**country_data)
        self.province = Province.objects.create(**province_data)
        self.district = District.objects.create(**district_data)
        self.sub_district = SubDistrict.objects.create(**sub_district_data)

    def test_country(self):
        country_data = {'name': 'United States', 'states': [],
                        'code': 'US', 'phone_code': '+1',
                        'currency_code': 'USD'}
        country = Country.objects.create(**country_data)

        self.assertTrue(isinstance(country, Country))
        self.assertEqual(country.__str__(), country.name)

    def test_province(self):
        province_data = {'name': 'Sumatera Utara',
                         'country_id': self.country.pk}
        province = Province.objects.create(**province_data)

        self.assertTrue(isinstance(province, Province))
        self.assertEqual(province.__str__(), province.name)

    def test_district(self):
        district_data = {'name': 'Ogan Komering Ulu',
                         'province_id': self.province.pk}
        district = District.objects.create(**district_data)

        self.assertTrue(isinstance(district, District))
        self.assertEqual(district.__str__(), district.name)

    def test_sub_district(self):
        sub_district_data = {'name': 'Kayuagung',
                             'district_id': self.district.pk,
                             'postal_code': '36422'}
        sub_district = SubDistrict.objects.create(**sub_district_data)

        self.assertTrue(isinstance(sub_district, SubDistrict))
        self.assertEqual(sub_district.__str__(), sub_district.name)
