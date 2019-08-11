# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.forms.models import model_to_dict
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from .utils import parse_json_string


class TimeStampedModel(models.Model):
    """
    TimeStampedModel

    An abstract base class model that provides self-managed
    "created_at", "updated_at" and "deleted_at" fields.
    """
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True


class DefaultManager(models.Manager):
    """
    Class to assign as ORM queryset manager,
    for example usage:

    class ModelName(models.Model):
        ...
        objects = DefaultManager()

    >>> ModelName.objects.published()
    >>> ModelName.objects.deleted()
    """

    def published(self):
        """ return queryset for not-deleted objects only. """
        return self.filter(deleted_at__isnull=True)

    def deleted(self):
        """ return queryset for deleted objects only. """
        return self.filter(deleted_at__isnull=False)


@python_2_unicode_compatible
class Country(TimeStampedModel):
    name = models.CharField(_('Name'), max_length=200)
    states = models.TextField(_('States'), null=True, blank=True,
                              help_text=_('List of states'))
    code = models.CharField(_('Code'), max_length=10, null=True, blank=True)
    phone_code = models.CharField(_('Phone Code'), max_length=10,
                                  null=True, blank=True)
    currency_code = models.CharField(_('Currency Code'), max_length=10,
                                     null=True, blank=True)

    objects = DefaultManager()

    def __str__(self):
        return self.name

    def get_states(self):
        """
        function to parse the `states` list string into list.
        :return list of states
        """
        return parse_json_string(self.states, default=[])

    class Meta:
        ordering = ('-id',)
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')


@python_2_unicode_compatible
class Province(TimeStampedModel):
    country = models.ForeignKey(Country, related_name='provinces',
                                on_delete=models.CASCADE,
                                verbose_name=_('Country'))
    name = models.CharField(_('Name'), max_length=200)

    objects = DefaultManager()

    def __str__(self):
        return self.name

    def get_districts(self):
        """
        function to get the districts related with this province.
        :return a queryset or None
        """
        if hasattr(self, 'districts'):
            return self.districts.published()
        return None

    class Meta:
        ordering = ('-id',)
        verbose_name = _('Province')
        verbose_name_plural = _('Provinces')


@python_2_unicode_compatible
class District(TimeStampedModel):
    province = models.ForeignKey(Province, related_name='districts',
                                 on_delete=models.CASCADE,
                                 verbose_name=_('Province'))
    name = models.CharField(_('Name'), max_length=200)

    objects = DefaultManager()

    def __str__(self):
        return self.name

    def get_sub_districts(self):
        """
        function to get the sub districts related with this district.
        :return a queryset or None
        """
        if hasattr(self, 'sub_districts'):
            return self.sub_districts.published()
        return None

    class Meta:
        ordering = ('-id',)
        verbose_name = _('District')
        verbose_name_plural = _('Districts')


@python_2_unicode_compatible
class SubDistrict(TimeStampedModel):
    district = models.ForeignKey(District, related_name='sub_districts',
                                 on_delete=models.CASCADE,
                                 verbose_name=_('District'))
    name = models.CharField(_('Name'), max_length=200)
    postal_code = models.CharField(_('Postal Code'), max_length=10,
                                   null=True, blank=True)

    objects = DefaultManager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-id',)
        verbose_name = _('Sub District')
        verbose_name_plural = _('Sub Districts')


class AddressModel(models.Model):
    """
    address class without any extending from another class.
    [i] usage example:

        class Profile(AddressModel, models.Model):
            pass

    [i] orm example:
        >>> profile.get_full_address(format_address='id', include_country=True)
        'Jl. Sudirman No.34, RT.4/RW.21 Sinduarjo, Ngaglik, Sleman, Yogyakarta, Indonesia - 55581'
        >>> profile.get_full_address_json()
        {
          "address": "Jl. Sudirman",
          "village": "Sinduarjo",
          "number": 34,
          "na": 4,
          "ca": 21,
          "sub_district": {
            "id": 1,
            "name": "Ngaglik",
            "postal_code": "55581",
          },
          "district": {
            "id": 1,
            "name": "Sleman",
          },
          "province": {
            "id": 1,
            "name": "Yogyakarta"
          },
          "country": {
            "id": 1,
            "name": "Indonesia",
            "code": "ID",
            "phone_code": "+62",
            "currency_code": "IDR",
            "states": [
              "Aceh",
              "Sumatera Utara",
              "Sumatera Barat",
              "Riau",
              ...
            ]
          }
        }
    """
    sub_district = models.ForeignKey(SubDistrict, on_delete=models.CASCADE,
                                     related_name='addresses',
                                     verbose_name=_('Sub District'))
    address = models.TextField(_('Address'))
    village = models.CharField(_('Village'), max_length=200, null=True, blank=True)
    number = models.IntegerField(_('Number'), null=True, blank=True)
    na = models.IntegerField(_('NA'), null=True, blank=True,
                             help_text=_('Neighborhood Association'))  # rt
    ca = models.IntegerField(_('CA'), null=True, blank=True,
                             help_text=_('Citizens Association'))  # rw

    def get_full_address(self, format_address='en', include_country=False):
        """
        function to get the complete address for this current model.

        >>> object.get_full_address(format_address='id', include_country=True)
        'Jl. Sudirman No.34, RT.4/RW.21 Sinduarjo, Ngaglik, Sleman, Yogyakarta, Indonesia - 55581'
        """
        def verbose_name(f): return self._meta.get_field(f).verbose_name

        na = self.na or '-'
        ca = self.ca or '-'
        na_label = 'RT' if format_address == 'id' else verbose_name('na')
        ca_label = 'RW' if format_address == 'id' else verbose_name('ca')
        number_label = 'No' if self.number and format_address == 'id' else verbose_name('number')
        number = ' %s.%s' % (number_label, self.number) if self.number else ''
        village = self.village or ''

        address_pattern = '%(address)s%(number)s, %(na_label)s.%(na)s/%(ca_label)s.%(ca)s %(village)s'.strip()
        address = address_pattern % {'address': self.address, 'number': number,
                                     'na_label': na_label, 'na': na,
                                     'ca_label': ca_label, 'ca': ca,
                                     'village': village}

        sub_district = self.sub_district
        postal_code = sub_district.postal_code
        district = sub_district.district
        province = district.province

        address_pattern = '%(address)s, %(sub_district)s, %(district)s, %(province)s'
        address = address_pattern % {'address': address, 'sub_district': sub_district,
                                     'district': district, 'province': province}

        if include_country:
            address = '%(address)s, %(country)s' % {'address': address,
                                                    'country': province.country}
        if postal_code:
            address = '%(address)s - %(postal_code)s' % {'address': address,
                                                         'postal_code': postal_code}
        return address

    def get_full_address_json(self):
        """
        function to get the json formated for complete address.

        >>> object.get_full_address_json()
        {
          "address": "Jl. Sudirman",
          "village": "Sinduarjo",
          "number": 34,
          "na": 4,
          "ca": 21,
          "sub_district": {
            "id": 1,
            "name": "Ngaglik",
            "postal_code": "55581"
          },
          "district": {
            "id": 1,
            "name": "Sleman"
          },
          "province": {
            "id": 1,
            "name": "Yogyakarta"
          },
          "country": {
            "id": 1,
            "name": "Indonesia",
            "code": "ID",
            "phone_code": "+62",
            "currency_code": "IDR",
            "states": [
              "Aceh",
              "Sumatera Utara",
              "Sumatera Barat",
              "Riau",
              ...
            ]
          }
        }
        """
        sub_district_data = model_to_dict(self.sub_district)
        district_data = model_to_dict(self.sub_district.district)
        province_data = model_to_dict(self.sub_district.district.province)
        country_data = model_to_dict(self.sub_district.district.province.country)
        country_data.update({'states': self.sub_district.district.province.country.get_states()})

        address = {'address': self.address, 'village': self.village,
                   'number': self.number, 'na': self.na, 'ca': self.ca}

        address['sub_district'] = sub_district_data
        address['district'] = district_data
        address['province'] = province_data
        address['country'] = country_data

        return address

    class Meta:
        abstract = True
