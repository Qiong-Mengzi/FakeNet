from dataclasses import dataclass, asdict
from typing import Any, Self, TypeVar


@dataclass(slots=True)
class MonoTag:
    @classmethod
    def mt_name(cls) -> str:
        return getattr(cls, "MT_NAME")

    def serialize(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def deserialize(cls, rawdata: dict[str, Any]) -> Self:
        return cls(**rawdata)


AnyMt = TypeVar("AnyMt", bound=MonoTag)


class _MtManager:
    def __init__(self):
        self.mt_types: dict[str, type[MonoTag]] = dict()

    def register(self, name: str):
        # TODO: `^[A-Za-z_][A-Za-z0-9]*:[A-Za-z_][A-Za-z0-9]*(/[A-Za-z_][A-Za-z0-9]*)*$`
        def wrap(mt_t: type[AnyMt]) -> type[AnyMt]:
            if name in self.mt_types:
                raise Exception

            self.mt_types[name] = mt_t
            setattr(mt_t, "MT_NAME", name)

            return mt_t

        return wrap

    def query(self, name: str) -> type[MonoTag] | None:
        return self.mt_types.get(name)


MtManager = _MtManager()
