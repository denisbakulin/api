from typing import Any, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import EntityAlreadyExists, EntityNotFoundError
from core.model import BaseORM
from core.repository import BaseRepository
from helpers.search import Pagination

T = TypeVar("T", bound=BaseORM)
R = TypeVar("R", bound=BaseRepository)


class BaseService[T, R]:
    """
    Базовый класс-service проекта
    с базовой бизнес-логикой для получения,
    удаления, проверки на существования объектов
    """

    def __init__(
            self,
            model: T,
            session: AsyncSession,
            repository: type[R] = None
    ):
        """При наследовании обязательно переопределить и указать модель,
        чтобы пользоваться методами класса"""

        self.model = model
        self.session = session
        if repository is not None:
            self.repository: R = repository(session=session)
        else:
            self.repository: R = BaseRepository(model, session)

    async def get_item_by_id(self, item_id: int) -> T:
        return await self.get_item_by(id=item_id)

    async def create_item(self, **params) -> T:
        item = self.repository.create(**params)

        await self.session.commit()
        await self.session.refresh(item)

        return item


    async def get_item_by(self, **params) -> T:
        """
        Возвращает запись по совпадениям params

        :raise
            EntityNotFoundError: Если запись не найдена
        """

        item = await self.repository.get_one_by(**params)

        if not item:
            raise EntityNotFoundError(
                self.model.__name__,
                **params
            )

        return item


    async def get_items_by(
            self,
            pagination: Pagination,
            **params
    ) -> list[T]:
        return await self.repository.get_any_by(**params, **pagination.dict())



    async def check_already_exists(self, **fields):
        """
        Проверяет на сущесвование записи

        :raise
            EntityAlreadyExists: Если запись существует
        """

        item = await self.repository.exists(**fields)

        if item:
            raise EntityAlreadyExists(
                entity=self.model.__name__,
                **fields
            )



    async def delete_item_by_id(self, item_id):
        """Удаляет запись по переданному id"""

        await self.repository.delete_by_id(item_id)


    async def delete_item(self, item: T):
        await self.repository.delete(item)


    async def update_item(self, item: T, **updates) -> T:
        await self.repository.update(item, **updates)
        await self.session.commit()
        await self.session.refresh(item)

        return item

    async def search_items(
            self,
            search,
            pagination: Pagination,
            inner_props: dict[str, Any] | None = None,
            **filters,
    ) -> list[T]:

        if search.strict:
            return await self.repository.get_any_by(
                **{search.field: search.q},
                **pagination.dict(),
                **filters,
                inner_props=inner_props,

            )
        return await self.repository.search(
            field=search.field,
            query=search.q,
            **pagination.dict(),
            **filters,
            inner_props=inner_props,
        )

