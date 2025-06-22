from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from main.core.application.forms.forms import EmailUpdateForm
from main.core.infrastructure.persistence.database.models import Collection


from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import redirect

class ProfileView:
    def handle_request(self, request: HttpRequest) -> HttpResponse:
        user = request.user
        collections = user.collections.all()

        current_collection = user.current_collection
        if current_collection:
            current_collection_id = current_collection.id
        else:
            current_collection_id = collections[0].id if collections else None

        if request.method == "POST":
            if "update_email" in request.POST:
                email_form = EmailUpdateForm(request.POST)
                if email_form.is_valid():
                    user.email = email_form.cleaned_data['email']
                    user.save()
                    messages.success(request, "Email mis à jour avec succès.")
                    return redirect('profile')
                password_form = PasswordChangeForm(user)
            elif "change_password" in request.POST:
                password_form = PasswordChangeForm(user, request.POST)
                if password_form.is_valid():
                    user = password_form.save()
                    update_session_auth_hash(request, user)  # Important pour garder la session
                    messages.success(request, "Mot de passe mis à jour avec succès.")
                    return redirect('profile')
                email_form = EmailUpdateForm(initial={'email': user.email})
        else:
            email_form = EmailUpdateForm(initial={'email': user.email})
            password_form = PasswordChangeForm(user)

        return render(request, 'profile/module.html', {
            'username': user.username,
            'first_name': user.first_name,
            'email': user.email,
            'current_collection_id': current_collection_id,
            'collections': [(collection.id, collection.title) for collection in collections],
            'email_form': email_form,
            'password_form': password_form,
        })

    def change_collection(self, request: HttpRequest, collection_id: int) -> HttpResponse:
        collection = get_object_or_404(Collection, id=collection_id, accounts=request.user)
        request.user.current_collection = collection
        request.user.save()
        return redirect('profile')


@login_required
def profile_view(request: HttpRequest) -> HttpResponse:
    view = ProfileView()
    return view.handle_request(request)


@login_required
def change_collection_view(request, collection_id):
    view = ProfileView()
    return view.change_collection(request, collection_id)
