from dataclasses import dataclass, asdict
from typing import Any, Self, TypeVar


@dataclass(slots=True)
class MonoTag:
    @classmethod
    def mt_name(cls) -> str:
        """获取组件类的注册名

        Returns:
            str: 组件类的注册名
        Raises:
            AttributeError: 无组件类注册名, 通常是组件未被注册引起的
        """
        return getattr(cls, "MT_NAME")

    def serialize(self) -> dict[str, Any]:
        """序列化组件

        Returns:
            dict[str, Any]: 序列化数据
        """
        return asdict(self)

    @classmethod
    def deserialize(cls, rawdata: dict[str, Any]) -> Self:
        """反序列化组件

        Args:
            rawdata (dict[str, Any]): 序列化的数据
        Returns:
            Self: 反序列化得到的组件实例
        Raises:
            TypeError: ?

        基类方法仅提供了基本的反序列化操作

        每个子类如果可能, 应该自行Override该方法
        """
        return cls(**rawdata)


AnyMt = TypeVar("AnyMt", bound=MonoTag)


class _MtManager:
    def __init__(self):
        self.mt_types: dict[str, type[MonoTag]] = dict()

    def register(self, name: str):
        """注册组件

        Args:
            name (str): 组件注册名

        Returns:
            Callable[[type[AnyMt]], type[AnyMt]]: 一个wrap函数

        Examples:
            >>> @MtManager.register('test:mt/pos')
            ... @dataclass(slots=True)
            ... class PosMt(MonoTag):
            ...   x: int
            ...   y: int

        该方法应作为装饰器使用
        """

        # TODO: `^[A-Za-z_][A-Za-z0-9]*:[A-Za-z_][A-Za-z0-9]*(/[A-Za-z_][A-Za-z0-9]*)*$`
        def wrap(mt_t: type[AnyMt]) -> type[AnyMt]:
            if name in self.mt_types:
                raise Exception

            self.mt_types[name] = mt_t
            setattr(mt_t, "MT_NAME", name)

            return mt_t

        return wrap

    def query(self, name: str) -> type[MonoTag] | None:
        """
        根据注册名查询组件

        Args:
            name (str): 注册名
        Returns:
            type[MonoTag] | None: 组件类, 如果不存在则为None
        """
        return self.mt_types.get(name)


MtManager = _MtManager()
