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
from django.contrib import admin
from django.urls import path
from main import views
from main.core.add_album.internal import add_album_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('bdrecherche/', views.bdrecherche, name='bdrecherche'),
    path('dedicace/', views.dedicace, name='dedicace'),
    path('pagebd/<int:isbn>/', views.pagebd, name='pagebd'),
    path('statistiques/', views.statistiques, name='statistiques'),
    path('upload/dedicace/<int:isbn>/', views.upload_dedicace, name='upload_dedicace'),
    path('upload/exlibris/<int:isbn>/', views.upload_exlibris, name='upload_exlibris'),
    path('delete/dedicace/<int:isbn>/<int:photo_number>', views.delete_dedicace, name='delete_dedicace'),
    path('delete/exlibris/<int:isbn>/<int:photo_number>', views.delete_exlibris, name='delete_exlibris'),
    path('add/<int:isbn>/', add_album_view, name='add_album'),
    path('update/', views.update_database, name='update'),
    path('possede/<int:isbn>/', views.possede, name='possede'),
]