from collections import defaultdict, deque
from typing import Callable, Iterable, Protocol

from .event import Event, ScheTickEvent


class ISubscriber(Protocol):
    def __call__(self, event: Event) -> Iterable[Event] | None: ...


Subsriber = ISubscriber | Callable[[Event], Iterable[Event] | None]


class Scheduler:
    SCHE_TICK = ScheTickEvent()

    def __init__(self, max_recursion_layer: int = 1000):
        self._max_recursion_layer = max_recursion_layer
        self.su: dict[type[Event], list[Subsriber]] = defaultdict(list[Subsriber])
        self.slots: deque[Event] = deque()

    def add_subscribers(self, event_type: type[Event], *s: Subsriber):
        self.su[event_type].extend(s)

    def put_event(self, e: Event):
        self.slots.append(e)

    def put_events(self, es: Iterable[Event]):
        self.slots.extend(es)

    def _get_events(self) -> Iterable[Event]:
        temp = self.slots
        self.slots = deque()
        return temp

    def tick(self):
        self.slots.appendleft(self.SCHE_TICK)
        layer_count: int = 0
        while len(self.slots) > 0:
            for e in self._get_events():
                for s in self.su.get(type(e), []):
                    r = s(e)
                    if r is not None:
                        self.put_events(r)

            layer_count += 1
            if layer_count >= self._max_recursion_layer:
                raise RecursionError
