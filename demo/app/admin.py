# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from app.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'full_address')
    fields = ('name', 'email', 'phone', 'sub_district',
              'village', 'number', 'na', 'ca', 'address')
    raw_id_fields = ('sub_district', )

    def full_address(self, profile):
        return profile.get_full_address(format_address='id', include_country=True)
    full_address.short_description = _('Full Address')
