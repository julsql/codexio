from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

from main.application.usecases.advanced_search.advanced_search_service import AdvancedSearchService
from main.application.usecases.random_attachment.random_attachment_service import RandomAttachmentService
from main.core.random_album.internal.random_album_view import random_album
from main.infrastructure.persistence.database.advanced_search_adapter import AdvancedSearchAdapter
from main.infrastructure.persistence.file.random_attachment_adapter import RandomAttachmentAdapter


def home(request: HttpRequest) -> HttpResponse:
    infos_album = random_album()
    random_attachment_repository = RandomAttachmentAdapter()
    random_attachment_service = RandomAttachmentService(random_attachment_repository)
    random_attachment = random_attachment_service.main()

    advanced_search_repository = AdvancedSearchAdapter()
    advanced_search_service = AdvancedSearchService(advanced_search_repository)
    advanced_search = advanced_search_service.main(request)

    if advanced_search.form_send:
        return render(request, 'bd_search/module.html',
                      {"banner_path": random_attachment.path, "banner_isbn": random_attachment.isbn,
                       "banner_type": random_attachment.type})

    return render(request, 'home/module.html',
                  {"banner_path": random_attachment.path, "banner_isbn": random_attachment.isbn,
                   "banner_type": random_attachment.type, "form": advanced_search.form, "random_album": infos_album})
