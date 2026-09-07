from dataclasses import dataclass, fields, asdict

@dataclass
class ManifestRequest:
    session_id: str
    iteration_l1: str
    iteration_l2: str
    iteration_l3: str
    iteration_l4: str

    @classmethod
    def required_fields(cls):
        return [field.name for field in fields(cls)]

    @classmethod
    def missing_fields(cls, payload: dict) -> list:
        if not payload:
            return cls.required_fields()
        return [
            field for field in cls.required_fields()
            if not payload.get(field)
        ]

    @classmethod
    def from_payload(cls, payload: dict) -> "ManifestRequest":
        return cls(**{field: payload.get(field) for field in cls.required_fields()})

    def to_dict(self) -> dict:
        return asdict(self)