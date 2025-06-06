from dataclasses import dataclass

from main.models import AppUser


@dataclass
class Collection:
    title: str
    accounts: list[AppUser]
