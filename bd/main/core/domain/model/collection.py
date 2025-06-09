from dataclasses import dataclass

from main.models import AppUser


@dataclass
class Collection:
    title: str
    accounts: list[AppUser]
    token: str
    doc_name: str
    sheet_name: str
