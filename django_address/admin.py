# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import (Country, Province, District, SubDistrict)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'phone_code', 'currency_code', 'created_at', 'deleted_at')
    list_filter = ('created_at', 'updated_at', 'deleted_at')
    search_fields = ('name', 'code', 'phone_code', 'currency_code', 'states')
    fields = ('name', 'states', 'code', 'phone_code', 'currency_code', 'deleted_at')


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'created_at', 'deleted_at')
    list_filter = ('created_at', 'updated_at', 'deleted_at')
    search_fields = ('name', 'country__name')
    raw_id_fields = ('country',)
    fields = ('name', 'country', 'deleted_at')


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'province', 'created_at', 'deleted_at')
    list_filter = ('created_at', 'updated_at', 'deleted_at')
    search_fields = ('name', 'province__name')
    raw_id_fields = ('province',)
    fields = ('name', 'province', 'deleted_at')


@admin.register(SubDistrict)
class SubDistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'district', 'province', 'created_at', 'deleted_at')
    list_filter = ('created_at', 'updated_at', 'deleted_at', 'district__province')
    search_fields = ('name', 'district__name')
    raw_id_fields = ('district',)
    fields = ('name', 'district', 'postal_code', 'deleted_at')

    def province(self, sub_district):
        return sub_district.district.province.name
    province.short_description = _('Province')
