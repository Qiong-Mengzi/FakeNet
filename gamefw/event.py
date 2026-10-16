from dataclasses import dataclass


@dataclass(slots=True)
class Event:
    pass


@dataclass(slots=True)
class QuitEvent(Event):
    pass


@dataclass(slots=True)
class ScheTickEvent:
    pass
