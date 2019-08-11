from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class DjangoAddressConfig(AppConfig):
    """
    Define config for the member app so that we can hook in signals.
    """
    name = 'django_address'
    verbose_name = _('Django Address')
