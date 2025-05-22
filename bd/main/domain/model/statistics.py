from dataclasses import dataclass


@dataclass
class Statistics:
    nombre_albums: int
    nombre_pages: int
    prix_total: float
    nombre_editions_speciales: int
    nombre_dedicaces: int
    nombre_exlibris: int

    @classmethod
    def empty(cls) -> 'Statistics':
        return cls(0, 0, 0.0, 0, 0, 0)
