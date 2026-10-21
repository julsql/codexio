from django.conf import settings
from django.http import HttpRequest


def site_url(request: HttpRequest) -> dict:
    return {'SITE_URL': settings.SITE_URL.rstrip('/')}
