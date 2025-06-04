from typing import Literal

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from main.application.usecases.attachments.attachments_service import AttachmentsService
from main.infrastructure.persistence.file.attachments_adapter import AttachmentsAdapter


def signed_copies_view(request: HttpRequest) -> HttpResponse:
    return attachment_view(request, "SIGNED_COPY")


def exlibris_view(request: HttpRequest) -> HttpResponse:
    return attachment_view(request, "EXLIBRIS")


def attachment_view(request: HttpRequest, attachment_type: Literal["SIGNED_COPY", "EXLIBRIS"]) -> HttpResponse:
    repository = AttachmentsAdapter()
    service = AttachmentsService(repository)
    if attachment_type == "SIGNED_COPY":
        attachments = service.main_signed_copies()
    else:
        attachments = service.main_ex_libris()

    return render(request, 'attachments/module.html', {
        'attachments': [{'isbn': attachment.isbn,
                         'album': attachment.title,
                         'number': attachment.number,
                         'series': attachment.series,
                         'range': attachment.range_attachment,
                         'attachments': attachment.total}
                        for attachment in attachments.attachments_list],
        'attachments_sum': attachments.sum,
        'title': attachments.title,
        'subtitle': attachments.subtitle,
        'image_path': attachments.image_path,
    })
