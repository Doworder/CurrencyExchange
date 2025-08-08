from dataclasses import fields
from typing import Type, TypeVar, Any

T = TypeVar('T')


class GetDTOFactory:
    @staticmethod
    def create(dto_class: Type[T], data: dict[str, Any]) -> T:
        return dto_class(**data)

    @staticmethod
    def create_list(dto_class: Type[T], data_list: list[dict[str, Any]]) -> list[T]:
        return [dto_class(**data) for data in data_list]

    @staticmethod
    def from_tuple(
            dto_class: Type[T],
            tuple_data: tuple[int, str|int, str|int, str|float]
    ) -> T:
        field_names = [f.name for f in fields(dto_class)]
        field_values = dict(zip(field_names, tuple_data))
        return dto_class(**field_values)

    @staticmethod
    def list_from_tuple(
            dto_class: Type[T],
            tuple_data: list[tuple[int,str|int, str|int, str|float]]
    ) -> list[T]:
        res = []
        field_names = [f.name for f in fields(dto_class)]
        for data in tuple_data:
            field_values = dict(zip(field_names, data))
            res.append(dto_class(**field_values))

        return res
