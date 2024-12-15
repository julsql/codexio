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
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static
from main.core.add_album.internal.add_album_view import add_album
from main.core.existing_album.internal.existing_album_view import existing_album
from main.core.update_database.internal.update_database_view import update_database
from main.core.upload_photo.internal.upload_photo_view import upload_dedicace, upload_exlibris
from main.core.delete_photo.internal.delete_photo_view import delete_dedicace, delete_exlibris
from main.core.statistics.internal.statistics_view import statistiques
from main.core.home.internal.home_view import home
from main.core.attachments.internal.attachments_view import attachments
from main.core.bd_search.internal.bd_search_view import bd_search
from main.core.page_bd.internal.page_bd_view import page_bd
from main.core.errors.internal.errors_view import error_500_view, error_404_view

handler500 = error_500_view
handler404 = error_404_view

urlpatterns = [
    path('', home, name='home'),
    path('bdrecherche/', bd_search, name='bdrecherche'),
    path('dedicace/', attachments, name='dedicace'),
    path('pagebd/<int:isbn>/', page_bd, name='pagebd'),
    path('statistiques/', statistiques, name='statistiques'),

    path('update/', update_database, name='update'),
    path('upload/dedicace/<int:isbn>/', upload_dedicace, name='upload_dedicace'),
    path('upload/exlibris/<int:isbn>/', upload_exlibris, name='upload_exlibris'),
    path('delete/dedicace/<int:isbn>/<int:photo_id>', delete_dedicace, name='delete_dedicace'),
    path('delete/exlibris/<int:isbn>/<int:photo_id>', delete_exlibris, name='delete_exlibris'),
    path('add/<int:isbn>/', add_album, name='add_album'),
    path('possede/<int:isbn>/', existing_album, name='possede'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
