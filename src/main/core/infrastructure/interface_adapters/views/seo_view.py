from django.conf import settings
from django.contrib.sitemaps import Sitemap
from django.http import HttpRequest, HttpResponse
from django.urls import reverse
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET

PRIVATE_PATHS = (
    '/admin/',
    '/accounts/',
    '/password-reset/',
    '/reset/',
    '/profile',
    '/change-collection/',
    '/recherche/',
    '/dedicaces/',
    '/exlibris/',
    '/ouvrage/',
    '/statistiques/',
    '/update/',
    '/upload/',
    '/delete/',
    '/add/',
    '/infos/',
    '/possede/',
    '/media/',
)


class PublicPagesSitemap(Sitemap):
    protocol = 'https'
    changefreq = 'monthly'

    def items(self) -> list[str]:
        return ['home', 'login']

    def location(self, item: str) -> str:
        return reverse(item)

    def priority(self, item: str) -> float:
        return 1.0 if item == 'home' else 0.5


SITEMAPS = {'pages': PublicPagesSitemap}


@require_GET
@cache_control(max_age=86400, public=True)
def robots_txt_view(request: HttpRequest) -> HttpResponse:
    lines = ['User-agent: *', 'Allow: /', 'Allow: /accounts/login/']
    lines += [f'Disallow: {path}' for path in PRIVATE_PATHS]
    lines += ['', f"Sitemap: {settings.SITE_URL.rstrip('/')}/sitemap.xml", '']
    return HttpResponse('\n'.join(lines), content_type='text/plain; charset=utf-8')
