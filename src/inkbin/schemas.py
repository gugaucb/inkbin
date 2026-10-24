from datetime import UTC, datetime, timedelta
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, field_validator

from inkbin.expiration import (
    calculate_expires_at,
    get_active_expiration_options,
    parse_duration_to_seconds,
)


class ExpirationValue(str):
    def to_datetime(self) -> datetime | None:
        return calculate_expires_at(str(self))

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: Any, handler: Any) -> Any:
        from pydantic_core import core_schema

        return core_schema.no_info_after_validator_function(cls, core_schema.str_schema())


class ExpirationEnum(str, Enum):
    one_hour = "1h"
    one_day = "1d"
    one_week = "1w"
    one_month = "1m"
    never = "never"

    def to_datetime(self) -> datetime | None:
        return calculate_expires_at(self.value)


class PasteCreateRequest(BaseModel):
    title: str | None = Field(default=None, max_length=200)
    content: str = Field(..., max_length=1_048_576)
    language: str = Field(default="plaintext", max_length=50)
    expiration: ExpirationValue = Field(default_factory=lambda: ExpirationValue("never"))
    password: str | None = Field(default=None, max_length=50)
    content_format: str = Field(default="plaintext", max_length=20)
    burn_after_read: bool = Field(default=False)

    @field_validator("content_format")
    @classmethod
    def validate_content_format(cls, value: str) -> str:
        valid_formats = {"plaintext", "aes-256-gcm", "base64"}
        if value not in valid_formats:
            raise ValueError(
                f"Formato de conteúdo '{value}' inválido. Valores permitidos: {', '.join(sorted(valid_formats))}."
            )
        return value

    @field_validator("expiration", mode="before")
    @classmethod
    def validate_expiration(cls, value: Any) -> ExpirationValue:
        active_options = get_active_expiration_options()
        if value is None or value == "":
            val_str = "never" if "never" in active_options else active_options[0]
            return ExpirationValue(val_str)

        val_str = getattr(value, "value", str(value)).strip()
        if val_str not in active_options:
            raise ValueError(
                f"Opção de expiração '{val_str}' não é permitida pelas configurações do sistema. Opções permitidas: {', '.join(active_options)}."
            )

        parse_duration_to_seconds(val_str)
        return ExpirationValue(val_str)

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
    content_format: str = "plaintext"
    burn_after_read: bool = False


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
    content_format: str = "plaintext"
    burn_after_read: bool = False


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
