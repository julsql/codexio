from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from main.core.infrastructure.persistence.database.models import Collection


@login_required
def profile_view(request: HttpRequest) -> HttpResponse:
    user = request.user
    collections = user.collections.all()

    current_collection = user.current_collection
    if current_collection:
        current_collection_id = current_collection.id
    else:
        current_collection_id = collections[0].id

    return render(request, 'profile/module.html',
                  {'username': user.username,
                   'first_name': user.first_name,
                   'email': user.email,
                   'current_collection_id': current_collection_id,
                   'collections': [(collection.id, collection.title) for collection in collections]
                   })


@login_required
def change_collection_view(request, collection_id):
    collection = get_object_or_404(Collection, id=collection_id, accounts=request.user)
    request.user.current_collection = collection
    request.user.save()
    return redirect('profile')
