from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotAllowed, HttpResponseNotFound, \
    HttpResponseBadRequest

CONTENT_TYPE = "text/plain; charset=utf-8"


class UTF8Response(HttpResponse):
    def __init__(self, content=None, status=200, *args, **kwargs):
        super().__init__(content, status=status, content_type=CONTENT_TYPE, *args, **kwargs)


class UTF8ResponseForbidden(HttpResponseForbidden):
    def __init__(self, content=None, *args, **kwargs):
        super().__init__(content, content_type=CONTENT_TYPE, *args, **kwargs)


class UTF8ResponseNotAllowed(HttpResponseNotAllowed):
    def __init__(self, permitted_methods, content=None, *args, **kwargs):
        super().__init__(permitted_methods, content, content_type=CONTENT_TYPE, *args, **kwargs)


class UTF8ResponseNotFound(HttpResponseNotFound):
    def __init__(self, content=None, *args, **kwargs):
        super().__init__(content, content_type=CONTENT_TYPE, *args, **kwargs)


class UTF8ResponseBadRequest(HttpResponseBadRequest):
    def __init__(self, content=None, *args, **kwargs):
        super().__init__(content, content_type=CONTENT_TYPE, *args, **kwargs)
