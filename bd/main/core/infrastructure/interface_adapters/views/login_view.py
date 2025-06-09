from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect

from main.core.application.forms.forms import LoginForm


class LoginView:
    def handle_request(self, request: HttpRequest) -> HttpResponse:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']

                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('home')
                else:
                    form.add_error(None, "Nom d'utilisateur ou mot de passe incorrect.")
        else:
            form = LoginForm()

        return render(request, 'login/module.html', {'form': form})


def login_view(request: HttpRequest) -> HttpResponse:
    view = LoginView()
    return view.handle_request(request)
