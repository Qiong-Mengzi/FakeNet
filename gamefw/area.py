from collections.abc import Iterable, Iterator

from .monotag import MonoTag

Archetype = frozenset[str]


class AreaData:
    def __init__(self, data_ref: dict[str, MonoTag]):
        self._data_ref = data_ref

    def __getitem__(self, key: str | type[MonoTag]):
        if isinstance(key, str):
            return self._data_ref[key]
        else:
            return self._data_ref[key.mt_name()]

    def __setitem__(self, key: str, value: MonoTag):
        if key not in self._data_ref:
            raise KeyError
        if key != value.mt_name():
            raise ValueError

        self._data_ref[key] = value

    def __contains__(self, item: str | type[MonoTag]):
        if isinstance(item, str):
            return item in self._data_ref
        else:
            return item.mt_name() in self._data_ref

    def update(self, value: MonoTag):
        if value.mt_name() not in self._data_ref:
            raise KeyError

        self._data_ref[value.mt_name()] = value


class AreaQuery(Iterable[int]):
    __slots__ = ("_arch", "_query_cache", "_cache_ver")

    def __init__(self, arch: Archetype, manager: "AreaManager"):
        if len(arch) == 0:
            raise ValueError

        self._arch = arch
        self._cache_ver: int = -1
        self._query_cache: set[int] = set()
        self._manager: "AreaManager" = manager

    def __iter__(self) -> Iterator[int]:
        self._resolve()
        return iter(self._query_cache)

    def _resolve(self):
        manager_ver = self._manager.get_cache_ver()
        if self._cache_ver == manager_ver:
            return

        self._query_cache = set[int].intersection(
            set(), *[self._manager.area_map.get(s, set()) for s in self._arch]
        )
        self._cache_ver = manager_ver


class AreaManager:
    def __init__(self):
        self.areas: dict[int, dict[str, MonoTag]] = dict()
        self.area_map: dict[str, set[int]] = dict()

        self.id_counter: int = 0
        self._ver: int = 0

        self._area_modify_cache: dict[int, dict[str, MonoTag] | None] = dict()

    def get_cache_ver(self) -> int:
        return self._ver

    def _gen_areaid(self) -> int:
        t = self.id_counter
        self.id_counter += 1
        return t

    def _remove_area(self, areaid: int):
        if areaid not in self.areas:
            return

        old_area_data = self.areas.pop(areaid)
        for mt_name in old_area_data.keys():
            # if mt_name in self.area_map:
            self.area_map[mt_name].discard(areaid)

    def _create_area(self, areaid: int, area_data_mov: dict[str, MonoTag]):
        self.areas[areaid] = area_data_mov
        for mt_name in area_data_mov.keys():
            if mt_name not in self.area_map:
                self.area_map[mt_name] = set()
            self.area_map[mt_name].add(areaid)

    def apply_area_modify(self):
        if len(self._area_modify_cache) == 0:
            return

        self._ver += 1

        for areaid, area_data in self._area_modify_cache.items():

            if area_data is None:  # 待移除的实体
                self._remove_area(areaid)
                continue

            # 待修改/添加的实体
            if areaid in self.areas:
                self._remove_area(areaid)
            self._create_area(areaid, area_data)

        self._area_modify_cache.clear()

    def create(self, init_data_mov: dict[str, MonoTag]):
        areaid = self._gen_areaid()
        self._area_modify_cache[areaid] = init_data_mov
        return areaid

    def remove(self, areaid: int):
        self._area_modify_cache[areaid] = None

    def modify(self, areaid: int, new_data_mov: dict[str, MonoTag]):
        if areaid not in self.areas and areaid not in self._area_modify_cache:
            raise KeyError
        self._area_modify_cache[areaid] = new_data_mov

    def access(self, areaid: int):
        if areaid in self.areas:
            return AreaData(self.areas[areaid])
        elif areaid in self._area_modify_cache:
            modified_data = self._area_modify_cache[areaid]
            if modified_data is None:
                raise RuntimeError
            return AreaData(modified_data)
        else:
            raise KeyError

    def query(self, arch: Archetype):
        return AreaQuery(arch, self)
