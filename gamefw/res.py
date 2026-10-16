from typing import Generic, TypeVar
import logging
from abc import ABC, abstractmethod

AnyRes = TypeVar("AnyRes")
LOGGER = logging.getLogger('gamefw.res')

class ResManager(ABC, Generic[AnyRes]):
    def __init__(self):
        self._reslist: dict[str, str] = dict()
        self._res_cache: dict[str, AnyRes] = dict()

    @abstractmethod
    def _loadres(self, key: str) -> AnyRes: ...

    def query_res(self, key: str) -> AnyRes | None:
        if key not in self._reslist:
            LOGGER.warning(f'Resource key {repr(key)} is not found')
            return None
        if key not in self._res_cache:
            self._res_cache[key] = self._loadres(key)
        return self._res_cache[key]

    def __contains__(self, item: str):
        return item in self._reslist

    def update_reslist(self, new_reslist: dict[str, str]):
        self._reslist = new_reslist.copy()
        self.clear_cache()

    def clear_cache(self):
        self._res_cache.clear()
