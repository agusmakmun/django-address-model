# -*- coding: utf-8 -*-
from __future__ import unicode_literals

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
