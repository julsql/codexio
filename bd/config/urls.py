"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns: path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path, include

from main.core.infrastructure.interface_adapters.views.add_album_view import add_album
from main.core.infrastructure.interface_adapters.views.attachments_view import exlibris_view, signed_copies_view
from main.core.infrastructure.interface_adapters.views.search_view import search_view
from main.core.infrastructure.interface_adapters.views.delete_photo_view import delete_dedicace, delete_exlibris
from main.core.infrastructure.interface_adapters.views.errors_view import error_500_view, error_404_view
from main.core.infrastructure.interface_adapters.views.existing_album_view import existing_album
from main.core.infrastructure.interface_adapters.views.home_view import home_view
from main.core.infrastructure.interface_adapters.views.login_view import login_view
from main.core.infrastructure.interface_adapters.views.work_view import work_view
from main.core.infrastructure.interface_adapters.views.profile_view import profile_view, change_collection_view
from main.core.infrastructure.interface_adapters.views.statistics_view import statistics_view
from main.core.infrastructure.interface_adapters.views.update_database_view import update_database
from main.core.infrastructure.interface_adapters.views.upload_photo_view import upload_dedicace_view, \
    upload_exlibris_view

handler500 = error_500_view
handler404 = error_404_view

urlpatterns = [
    path('accounts/login/', login_view, name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),

    path('', home_view, name='home'),
    path('profile', profile_view, name='profile'),
    path('change-collection/<int:collection_id>/', change_collection_view, name='change_collection'),
    path('recherche/', search_view, name='recherche'),
    path('dedicaces/', signed_copies_view, name='dedicaces'),
    path('exlibris/', exlibris_view, name='exlibris'),
    path('ouvrage/<int:isbn>/', work_view, name='ouvrage'),
    path('statistiques/', statistics_view, name='statistiques'),

    path('update/', update_database, name='update'),
    path('upload/dedicace/<int:isbn>/', upload_dedicace_view, name='upload_dedicace'),
    path('upload/exlibris/<int:isbn>/', upload_exlibris_view, name='upload_exlibris'),
    path('delete/dedicace/<int:isbn>/<int:photo_id>', delete_dedicace, name='delete_dedicace'),
    path('delete/exlibris/<int:isbn>/<int:photo_id>', delete_exlibris, name='delete_exlibris'),
    path('add/<int:isbn>/', add_album, name='add_album'),
    path('possede/<int:isbn>/', existing_album, name='possede'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
