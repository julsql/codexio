from main.domain.exceptions.domain_exceptions import DomainException


class SheetException(DomainException):
    """Exception de base pour Google Sheets"""

    def __init__(self, message: str):
        super().__init__(message)


class SheetConnexionException(SheetException):
    """Google Sheets non accessible"""
    pass
