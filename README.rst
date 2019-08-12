=====================
Django Address Model
=====================

|pypi version| |license| |build status|

django abstract model that provide the complete address, eg: no, na/rt, ca/rw, village,
sub district, district, province, country, postal code, currency code, phone code, etc.


.. image:: https://i.imgur.com/5mV5Jje.png


**Support Languages**

1. ID - Indonesia


Quick start
-----------

1. Django Log Viewer is available directly from `PyPI`_:

::

    pip install django-address-model


2. Add ``"django_address"`` to your ``INSTALLED_APPS`` setting like this

::

    INSTALLED_APPS = [
        ...
        "django_address",
    ]


3. Create an initial address

::

    python manage.py create_address --language=id --show-print=true



Usage Example
-------------

In your ``models.py``

::

    from django.db import models
    from django_address.models import AddressModel


    class Profile(AddressModel, models.Model):
        name = models.CharField(max_length=100)
        email = models.EmailField(blank=True, null=True)
        phone = models.CharField(max_length=15, blank=True, null=True)

        def __str__(self):
            return self.name

        class Meta:
            ordering = ('-id',)


`ORM Usage Example`


::

    >>> from django_address.models import SubDistrict
    >>> from app.models import Profile
    >>>
    >>> sub_district = SubDistrict.objects.first()
    >>> profile_data {'name': 'Summon Agus', 'email': 'summon@mail.com', 'phone': '+6282133338888',
                      'address': 'Jl. Karto Dimejo', 'number': 35, 'na': 3, 'ca': 34, 'village': 'Sinduarjo',
                      'sub_district': sub_district}
    >>> profile = Profile.objects.create(**profile_data)
    >>> profile.number
    35
    >>> profile.address
    'Jl. Karto Dimejo'
    >>> profile.village
    'Sinduarjo'
    >>> profile.sub_district
    'Ngaglik'
    >>> profile.sub_district.district
    'Sleman'
    >>> profile.get_full_address(format_address='id', include_country=True)
    'Jl. Karto Dimejo No.35, RT.3/RW.34 Sinduarjo, Ngaglik, Sleman, Yogyakarta, Indonesia - 55581'
    >>>
    >>> profile.get_full_address_json()
    {
      'na': 3,
      'ca': 34,
      'number': 35,
      'village': 'Sinduarjo',
      'address': 'Jl. Karto Dimejo',
      'sub_district': {
        'id': 1,
        'district': 1,
        'deleted_at': None,
        'postal_code': '55581',
        'name': 'Ngaglik'
      },
      'district': {
        'id': 1,
        'name': 'Sleman',
        'deleted_at': None,
        'province': 1
      },
      'province': {
        'id': 1,
        'name': 'Yogyakarta',
        'deleted_at': None,
        'country': 1
      },
      'country': {
        'id': 1,
        'phone_code': '+62',
        'deleted_at': None,
        'name': 'Indonesia',
        'currency_code': 'IDR',
        'code': 'ID',
        'states': [
          'Aceh',
          'Bali',
          'Banten',
          'Bengkulu',
          'Gorontalo',
          'Jakarta',
          'Jambi',
          'Jawa Barat',
          'Jawa Tengah',
          'Jawa Timur',
          'Kalimantan Barat',
          'Kalimantan Selatan',
          'Kalimantan Tengah',
          'Kalimantan Timur',
          'Kalimantan Utara',
          'Kepulauan Bangka Belitung',
          'Kepulauan Riau',
          'Lampung',
          'Maluku',
          'Maluku Utara',
          'Nusa Tengga     ra Barat',
          'Nusa Tenggara Timur',
          'Papua (Irian Jaya)',
          'Papua Barat',
          'Riau',
          'Sulawesi Barat',
          'Sulawesi Selatan',
          'Sulawesi Tengah',
          'Sulawesi Tenggara',
          'Sulawesi Utara',
          'Sumatera Barat',
          'Sumatera Selatan',
          'Sumatera Utara',
          'Yogyakarta'
        ]
      }
    }
    >>>


.. |pypi version| image:: https://img.shields.io/pypi/v/django-address-model.svg
   :target: https://pypi.python.org/pypi/django-address-model

.. |license| image:: https://img.shields.io/badge/license-MIT-green.svg
   :target: https://raw.githubusercontent.com/agusmakmun/django-address-model/master/LICENSE

.. |build status| image:: https://travis-ci.org/agusmakmun/django-address-model.svg?branch=master
   :target: https://travis-ci.org/agusmakmun/django-address-model

.. _`PyPI`: https://pypi.python.org/pypi/django-address-model
