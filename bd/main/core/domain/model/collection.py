from dataclasses import dataclass

from main.core.infrastructure.persistence.database.models import AppUser
from main.core.infrastructure.persistence.database.models.profile import Profile


@dataclass
class Collection:
    title: str
    token: str
    doc_name: str
    sheet_name: str
    accounts: list[AppUser]
    profile: Profile
