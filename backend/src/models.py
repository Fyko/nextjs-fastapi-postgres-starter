import enum
from datetime import datetime, timezone
from typing import List

from sqlalchemy import DateTime, Enum, ForeignKey, String, event
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )

    @staticmethod
    def _update_timestamp(_mapper, _connection, target):
        target.updated_at = datetime.now(timezone.utc)

    @classmethod
    def __declare_last__(cls):
        event.listen(cls, "before_update", cls._update_timestamp)


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128))

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}"


class MessageSender(enum.Enum):
    human = "human"
    system = "system"


class Message(Base):
    __tablename__ = "message"

    id: Mapped[int] = mapped_column(primary_key=True)
    thread_id: Mapped[int] = mapped_column(ForeignKey("thread.id"))
    sender: Mapped[MessageSender] = mapped_column(Enum(MessageSender))
    content: Mapped[str] = mapped_column(String(2048))

    thread: Mapped["Thread"] = relationship(back_populates="messages")

    def __repr__(self) -> str:
        return f"Message(id={self.id!r}, thread_id={self.thread_id!r}, sender={self.sender!r}, content={self.content!r})"


class Thread(Base):
    __tablename__ = "thread"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(128), nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    messages: Mapped[List["Message"]] = relationship(
        back_populates="thread", lazy="joined"
    )

    def __repr__(self) -> str:
        return f"Thread(id={self.id!r}, title={self.title!r}, user_id={self.user_id!r}, messages={self.messages!r})"
