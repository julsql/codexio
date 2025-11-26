from dataclasses import dataclass


@dataclass
class AppUser:
    username: str
    password: str
    first_name: str
    email: str
