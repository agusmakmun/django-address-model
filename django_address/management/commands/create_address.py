# -*- coding: utf-8 -*-

import os
import sys
import json

from django.utils import timezone
from django.core.management.base import BaseCommand
from django.utils.translation import ugettext_lazy as _

from django_address.models import (Country, Province,
                                   District, SubDistrict)

MANAGEMENT_DIR = os.path.dirname(os.path.dirname(__file__))
DJANGO_ADDRESS_PATH = '/'.join(MANAGEMENT_DIR.split('/')[:-1])


class Command(BaseCommand):
    """
    Command to generate an initial address.

    ./manage.py create_address
    """

    help = _('Command to generate an initial address')

    def add_arguments(self, parser):
        parser.add_argument('-language', '--language', default='id',
                            help=_('Language code of country'))
        parser.add_argument('-show-print', '--show-print', default=False,
                            help=_('To show the print or not'))
        return parser

    def create_countries(self, show_print=False):
        """
        function to sync the countries data.

        :param `show_print` is boolean to enable or disable the print out.
        """
        countries_path = os.path.join(DJANGO_ADDRESS_PATH, 'fixtures/countries.json')
        countries_code_path = os.path.join(DJANGO_ADDRESS_PATH, 'fixtures/countries-code.json')

        # clear all countries
        Country.objects.all().delete()

        countries_list = json.load(open(countries_path)).get('countries', [])
        for country_data in countries_list:
            country, created = Country.objects.get_or_create(
                name=country_data.get('country'),
                states=json.dumps(country_data.get('states') or []),
                deleted_at=timezone.now()
            )

            if show_print:
                print(_('[+] Created a country %(country)s') % {'country': country})

        countries_code_list = json.load(open(countries_code_path))
        for country_data in countries_code_list:
            countries = Country.objects.filter(name__iexact=country_data.get('name'))\
                                       .update(code=country_data.get('code'),
                                               phone_code=country_data.get('phone_code'),
                                               currency_code=country_data.get('currency_code'))
            if show_print:
                print(_('[*] Updated a country %(country_data)s') % {'country_data': country_data})

        return countries_list

    def create_addresses(self, language='id', show_print=False):
        """
        function to sync the address with province, district, and sub_district.

        :param `language` is string language code / country code.
        :param `show_print` is boolean to enable or disable the print out.
        """
        language_path = 'fixtures/languages/%s/addresses.json' % language
        addresses_path = os.path.join(DJANGO_ADDRESS_PATH, language_path)

        if not os.path.exists(addresses_path):
            print(_('[!] Language code "%(lang)s" doesn\'t available!') % {'lang': language})
            print(_('[!] We really opened if you want to contribute and support your language.'))
            print(_('[i] Please visit: "https://github.com/agusmakmun/django-address-model" to contribute.'))
            sys.exit(0)

        addresses_data = json.load(open(addresses_path))
        country = Country.objects.get(name__iexact=addresses_data.get('country'))

        # clear all address
        SubDistrict.objects.all().delete()
        District.objects.all().delete()
        Province.objects.all().delete()

        provinces_dict = {}
        for province_code, province_data in addresses_data.get('provinces', {}).items():
            province_name = province_data.get('province_name')
            province, created = Province.objects.get_or_create(country=country,
                                                               name=province_name)
            provinces_dict.update({province_code: province})

            if show_print:
                print(_('[+] Created a province %(province)s') % {'province': province})

        for province_code, postal_list_data in addresses_data.get('postals', {}).items():
            province = provinces_dict.get(province_code)

            for postal_data in postal_list_data:
                district_name = postal_data.get('city')
                district, created = District.objects.get_or_create(province=province,
                                                                   name=district_name)

                postal_code = postal_data.get('postal_code')
                sub_district_name = postal_data.get('sub_district')
                sub_district, created = SubDistrict.objects.get_or_create(district=district,
                                                                          name=sub_district_name,
                                                                          postal_code=postal_code)
                if show_print:
                    print(_('[+] Created a %(district)s > %(sub_district)s') % {'district': district,
                                                                                'sub_district': sub_district})

    def handle(self, *args, **kwargs):
        # to
        language = kwargs.get('language')
        language = str(language).lower() if language else 'id'

        # to enable the print or not
        show_print = kwargs.get('show_print')
        show_print = True if str(show_print).lower() == 'true' else False

        self.create_countries(show_print)
        self.create_addresses(language, show_print)
