from dataclasses import dataclass, field


@dataclass
class BdAttachment:
    dedicaces: list[str] = field(default_factory=list)
    ex_libris: list[str] = field(default_factory=list)

    def __str__(self) -> str:
        return f"BdAttachment(dedicaces={', '.join(self.dedicaces)}, ex_libris={', '.join(self.ex_libris)})"
