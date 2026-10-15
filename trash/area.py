"""实体管理器

gamefw.area

! 这是一份有问题的代码, DO NOT USE !
"""

from collections.abc import Iterable
from typing import cast

from .monotag import MonoTag


class AreaQuery:
    """实体查询对象

    很可惜Python没有移动语义, 否则小恶魔要上unique_ptr<>了()
    """

    def __init__(self, mt_types: Iterable[str], areas_wref: set[int]):
        self.mt_types: frozenset[str] = frozenset(mt_types)
        self.area_cache_wref = areas_wref

    def query(self):
        return iter(self.area_cache_wref)


class AreaData:
    def __init__(self, data: dict[str, MonoTag]):
        self.data = data

    def __getitem__(self, key: str | type[MonoTag]):
        if isinstance(key, str):
            return self.data[key]
        else:
            return self.data[key.mt_name()]

    def __setitem__(self, key: str, value: MonoTag):
        if key not in self.data:
            raise KeyError
        if key != value.mt_name():
            raise ValueError
        self.data[key] = value

    def put_mt(self, value: MonoTag):
        if value.mt_name() not in self.data:
            raise KeyError
        self.data[value.mt_name()] = value

    def __contains__(self, item: str | type[MonoTag]):
        return (
            item in self.data if isinstance(item, str) else item.mt_name() in self.data
        )


Archetype = frozenset[str]


class AreaManager:
    """
    实体(Area)管理器

    根据观测结果, 实体的查询遍历操作较增删操作多得多

    故而缓存实体的组件关系是十分有必要的

    ---

    并不打算复用areaid

    感觉这个东西挺过度设计的......
    """

    def __init__(self):
        # {areaid: {mt_name: mt_data}}
        self.areas: dict[int, dict[str, MonoTag]] = dict()
        # {mt_name: areaid{}}
        self.area_map: dict[str, set[int]] = dict()

        # {arch: unique<areaid>@areas{}}
        # 这里的set[int]是AreaManager的
        self.query_reg: dict[Archetype, set[int]] = dict()
        self.arch_map: dict[str, set[Archetype]] = dict()

        self.areaid_counter: int = 0

    def _gen_areaid(self) -> int:
        t = self.areaid_counter
        self.areaid_counter += 1
        return t

    def _recalc_arch(self, arch: Archetype):
        return set[int].union(*[self.area_map[mt_name] for mt_name in arch])

    def create(self, init_data_mov: dict[str, MonoTag]) -> int:
        areaid = self._gen_areaid()
        self.areas[areaid] = init_data_mov

        for mt_name in init_data_mov.keys():
            if mt_name not in self.area_map:
                self.area_map[mt_name] = set()
            self.area_map[mt_name].add(areaid)

            for arch in self.arch_map.get(mt_name, cast(list[Archetype], [])):
                if arch in self.query_reg:
                    self.query_reg[arch].add(areaid)

        return areaid

    def access(self, areaid: int) -> AreaData:
        return AreaData(self.areas[areaid].copy())

    def remove(self, areaid: int):
        data = self.areas.pop(areaid)
        for mt_name in data.keys():
            if mt_name in self.area_map:
                self.area_map[mt_name].discard(areaid)

            for arch in self.arch_map.get(mt_name, cast(list[Archetype], [])):
                if arch in self.query_reg:  # 理论上不应该没有
                    self.query_reg[arch].discard(areaid)

    def query(self, arch: Archetype):
        if arch not in self.query_reg:
            for arch_part in arch:
                if arch_part not in self.arch_map:
                    self.arch_map[arch_part] = set()
                self.arch_map[arch_part].add(arch)

            areas_cur = self._recalc_arch(arch)
            self.query_reg[arch] = areas_cur
            query_inst = AreaQuery(arch, areas_cur)
            return query_inst
        else:
            return AreaQuery(arch, self.query_reg[arch])
