from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domain.entities.responses import ResponseEntity
from infra.repositories.alchemy_models.base import TimedBaseModel

if TYPE_CHECKING:
    from infra.repositories.alchemy_models.jobs import Job
    from infra.repositories.alchemy_models.users import User


class Response(TimedBaseModel):
    message: Mapped[str] = mapped_column(Text, comment="Описание вакансии")
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), comment="Идентификатор пользователя")
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id"), comment="Идентификатор вакансии")

    user: Mapped["User"] = relationship(back_populates="responses", )
    job: Mapped["Job"] = relationship(back_populates="responses", )

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id},"

    def __repr__(self):
        return str(self)

    def to_entity(self) -> ResponseEntity:
        return ResponseEntity(
            id=self.id,
            message=self.message,
            user_id=self.user_id,
            job_id=self.job_id,
            created_at=self.created_at,
        )