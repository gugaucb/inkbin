from datetime import UTC, datetime, timedelta
from enum import Enum

from pydantic import BaseModel, Field, field_validator


class ExpirationEnum(str, Enum):
    one_hour = "1h"
    one_day = "1d"
    one_week = "1w"
    one_month = "1m"
    never = "never"

    def to_datetime(self) -> datetime | None:
        now = datetime.now(UTC)
        match self:
            case ExpirationEnum.one_hour:
                return now + timedelta(hours=1)
            case ExpirationEnum.one_day:
                return now + timedelta(days=1)
            case ExpirationEnum.one_week:
                return now + timedelta(weeks=1)
            case ExpirationEnum.one_month:
                return now + timedelta(days=30)
            case ExpirationEnum.never:
                return None


class PasteCreateRequest(BaseModel):
    title: str | None = Field(default=None, max_length=200)
    content: str = Field(..., max_length=1_048_576)
    language: str = Field(default="plaintext", max_length=50)
    expiration: ExpirationEnum = Field(default=ExpirationEnum.never)
    password: str | None = Field(default=None, max_length=50)

    @field_validator("content")
    @classmethod
    def validate_content_not_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("O conteúdo do paste não pode ser vazio ou conter apenas espaços.")
        if len(value.encode("utf-8")) > 1_048_576:
            raise ValueError("O conteúdo excede o tamanho máximo de 1MB permitido.")
        return value

    @field_validator("password", mode="before")
    @classmethod
    def validate_password_length(cls, value: str | None) -> str | None:
        if value is None or (isinstance(value, str) and not value.strip()):
            return None
        value = value.strip()
        if len(value) < 4 or len(value) > 50:
            raise ValueError("A senha deve ter entre 4 e 50 caracteres.")
        return value


class PasteCreateResponse(BaseModel):
    slug: str
    url: str
    admin_delete_token: str
    title: str | None
    language: str
    expires_at: datetime | None
    created_at: datetime
    is_protected: bool = False


class PasteDetailResponse(BaseModel):
    slug: str
    title: str | None
    content: str
    language: str
    views_count: int
    expires_at: datetime | None
    created_at: datetime
    is_protected: bool = False
    is_active: bool = True


class PasteUnlockRequest(BaseModel):
    password: str = Field(..., min_length=1, max_length=100)


class PasteUnlockResponse(BaseModel):
    message: str
    unlocked: bool
    slug: str


class ReportReasonEnum(str, Enum):
    spam = "spam"
    malware = "malware"
    leak = "leak"
    abuse = "abuse"
    other = "other"


class PasteReportRequest(BaseModel):
    reason: ReportReasonEnum
    details: str | None = Field(default=None, max_length=1000)


class PasteReportResponse(BaseModel):
    message: str
    slug: str
    report_count: int
