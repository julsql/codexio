from typing import Literal

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from main.core.infrastructure.logging.python_logger_adapter import PythonLoggerAdapter


class ErrorView:
    def __init__(self):
        self.logger_adapter = PythonLoggerAdapter()

    def handle_error(self, request: HttpRequest, code: Literal[404, 500], exception: Exception = None) -> HttpResponse:
        if exception:
            self.logger_adapter.error(f"{code} Error: {exception}")
        else:
            self.logger_adapter.error(f"{code} Error")

        return render(request, f'errors/{code}.html', status=code)


def error_404_view(request: HttpRequest, exception: Exception) -> HttpResponse:
    view = ErrorView()
    return view.handle_error(request, 404, exception)


def error_500_view(request: HttpRequest) -> HttpResponse:
    view = ErrorView()
    return view.handle_error(request, 500)
