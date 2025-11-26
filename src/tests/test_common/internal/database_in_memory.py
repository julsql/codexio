from typing import Dict

from django.contrib.auth.base_user import AbstractBaseUser

from main.core.domain.ports.repositories.table_bd_repository import DatabaseRepository
from main.models import AppUser


class DatabaseInMemory(DatabaseRepository):
    def __init__(self):
        self.database = None
        self.column_names = None

    def reset_table(self, user: AbstractBaseUser) -> None:
        self.database = []

    def insert(self, value: list[Dict[str, str]], user: AppUser) -> None:
        self.database = value

    def get_all(self) -> list:
        return self.database
