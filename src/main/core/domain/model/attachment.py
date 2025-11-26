from dataclasses import dataclass, field


@dataclass
class Attachment:
    isbn: int
    title: str = ""
    number: str = ""
    series: str = ""
    total: int = 0
    range_attachment: range = field(init=False)

    def __post_init__(self):
        self.range_attachment = range(1, self.total + 1)

    def __str__(self):
        return f"Attachment(isbn={self.isbn}, title={self.title}, number={self.number}, series={self.series}, " \
               f"total={self.total}, range_attachment={self.range_attachment})"
