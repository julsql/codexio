from dataclasses import dataclass, field


@dataclass
class WorkAttachment:
    signed_copies: list[str] = field(default_factory=list)
    ex_libris: list[str] = field(default_factory=list)

    def __str__(self) -> str:
        return f"WorkAttachment(signed_copies={', '.join(self.signed_copies)}, ex_libris={', '.join(self.ex_libris)})"
