from typing import Generic, TypeVar


class MoveError(Exception):
    pass


T = TypeVar("T")


class Selfish(Generic[T]):
    __slots__ = ("_data", "_owner")

    def __init__(self, data: T):
        self._data: T = data
        self._owner: bool = False

    @property
    def data(self) -> T:
        if not self._owner:
            raise MoveError("Value has been moved.")
        return self._data

    def move(self) -> "Selfish[T]":
        if not self._owner:
            raise MoveError("Value has already been moved.")

        self._owner = False
        data = self._data
        self._data = None  # type: ignore

        inst = Selfish(data)
        inst._owner = True
        return inst

    def is_owner(self) -> bool:
        return self._owner


def selfish_of(data: T) -> Selfish[T]:
    inst = Selfish(data)
    inst._owner = True  # type: ignore
    return inst
