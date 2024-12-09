from django.shortcuts import render

from main.core.advanced_search.internal.advanced_search_view import advanced_search
from main.core.random_album.internal.random_album_view import random_album
from main.core.random_dedicace.internal.random_dedicace_view import random_dedicace


def home(request):
    infos_album = random_album()
    banner = random_dedicace()
    form, _, form_send = advanced_search(request)
    value = banner.copy()
    if form_send:
        return render(request, 'bd_search/module.html', value)
    value.update({'form': form, 'infos': infos_album})
    return render(request, 'home/module.html', value)
