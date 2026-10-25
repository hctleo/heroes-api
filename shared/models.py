from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
from uuid import UUID, uuid4


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class BaseModel(SQLModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=utc_now, nullable=False)
    updated_at: datetime = Field(
        default_factory=utc_now,
        nullable=False,
        sa_column_kwargs={"onupdate": utc_now},
    )
    deleted_at: datetime | None = Field(default=None)

    def soft_delete(self):
        self.deleted_at = utc_now()
