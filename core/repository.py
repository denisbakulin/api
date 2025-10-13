from typing import Any, Optional, TypeVar, Unpack

from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute

from core.model import BaseORM

T = TypeVar("T", bound=BaseORM)
Q = TypeVar("Q") #Любой sqlalchemy запрос

class BaseRepository[T]:
    """Базовый класс-repository проекта
    для взаимодействия с БД с
    операциями создания, получения, удаления записи
    """

    def __init__(self, model: T, session: AsyncSession):
        """При наследовании обязательно переопределить и указать модель,
        чтобы пользоваться методами класса"""

        self.model = model
        self.session = session


    async def get_any_by(
            self,
            offset: int | None = None,
            limit: int | None = None,
            lines: list | None = None,
            order_by: str = "id",
            _desc: bool = True,
            inner_props: dict[str, Any] = None,
            **filters,
    ) -> list[T] | list[Any]:
        """Возвращает отфильтрованный и отсортированый список записей
        по заданным параметрам и фильтрам
       """

        if lines:
            stmt = select(*lines)
        else:
            stmt = select(self.model)

        if filters:
            stmt = stmt.filter_by(**filters)

        if inner_props:
            stmt = self._process_stmt_with_inner_fields(inner_props, stmt)

        order_func = getattr(self.model, order_by, None)

        if order_func is not None:
            stmt = stmt.order_by(desc(order_func) if _desc else order_func)

        if offset:
            stmt = stmt.offset(offset)

        if limit:
            stmt = stmt.limit(limit)

        result = await self.session.execute(stmt)

        if lines:
            return [*result.all()]

        return [*result.scalars().all()]


    async def get_one_by(
            self,
            inner_props: dict[str, Any] = None,
            **filters
    ) -> Optional[T]:
        """Возвращает уникальную запись или None по указанным параметрам,
        если > 1 - Ошибка"""

        stmt = select(self.model).filter_by(**filters)

        stmt = self._process_stmt_with_inner_fields(inner_props, stmt)

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()


    def create(
            self,
            **data
    ) -> T:
        """Создает запись"""

        item = self.model(**data)
        self.session.add(item)
        return item

    async def exists(
            self,
            **filters
    ) -> bool:
        """Проверяет существование записи"""

        result = await self.get_one_by(**filters)
        return bool(result)


    async def delete_by_id(
            self,
            item_id: int
    ):
        """Удаляет запись по id"""

        item = await self.get_one_by(id=item_id)
        await self.delete(item)

    async def delete(
            self,
            item: T
    ):
        """Удаляет запись без подтверждения сверху (commit)"""

        await self.session.delete(item)
        await self.session.commit()


    async def get_items_count(self, **filters) -> int:
        """Возврвщвет количество записей в таблице"""

        stmt = select(func.count()).select_from(self.model)

        if filters:
            stmt = stmt.filter_by(**filters)

        count = await self.session.execute(stmt)
        return count.scalar_one()

    async def update(self, item: T, **updates) -> T:
        for key, value in updates.items():
            setattr(item, key, value)

        return item


    async def search(
        self,
        field: str,
        query: Any,
        offset: int,
        limit: int,
        inner_props: dict[str, Any] | None = None,
    ) -> list[T]:
        stmt = select(self.model).where(getattr(self.model, field).ilike(f"%{query}%"))

        stmt = self._process_stmt_with_inner_fields(inner_props, stmt)

        stmt = stmt.offset(offset).limit(limit)

        result = await self.session.execute(stmt)

        return list(result.scalars().all())


    def _process_stmt_with_inner_fields(self, inner_props: dict[str, Any] | None, stmt: Q) -> Q:
        """
        Добавляет join и фильтры по вложенным свойствам (One-to-One / One-to-Many)
        inner_props = {"settings.show_in_search": True}
        """

        if not inner_props:
            return stmt

        for prop_path, value in inner_props.items():
            parts = prop_path.split(".")
            current_model = self.model
            rel_attr = getattr(current_model, parts[0])

            # join с таблицей
            stmt = stmt.join(rel_attr)

            # проход по вложенным уровням (если есть)
            for part in parts[1:-1]:
                rel_class = rel_attr.property.mapper.class_
                rel_attr = getattr(rel_class, part)
                stmt = stmt.join(rel_attr)

            # фильтр по последнему полю
            rel_class = rel_attr.property.mapper.class_
            column = getattr(rel_class, parts[-1])
            stmt = stmt.where(column == value)

        return stmt






