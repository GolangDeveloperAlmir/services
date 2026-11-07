"""Environment-backed settings with startup validation for production security."""

from ipaddress import ip_address
from pathlib import Path
from urllib.parse import urlsplit
from typing import Literal, Self

from pydantic import AliasChoices, Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


DEFAULT_MEDIA_ROOT = Path(__file__).resolve().parents[2] / "media"


class Settings(BaseSettings):
    """Application configuration loaded from environment and optional .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        hide_input_in_errors=True,
    )

    app_name: str = "User Service"
    app_env: Literal["development", "test", "production"] = "development"
    database_url: str
    redis_url: str
    allowed_hosts: list[str] = Field(
        default=["localhost", "127.0.0.1", "::1"],
        validation_alias=AliasChoices("APP_ALLOWED_HOSTS", "allowed_hosts"),
    )
    trusted_proxy_ips: list[str] = Field(
        default_factory=list,
        validation_alias=AliasChoices("APP_TRUSTED_PROXY_IPS", "trusted_proxy_ips"),
    )
    media_root: Path = Field(
        default=DEFAULT_MEDIA_ROOT,
        validation_alias=AliasChoices("APP_MEDIA_ROOT", "media_root"),
    )
    auth_session_ttl_seconds: int = Field(default=900, ge=60, le=3600)
    auth_rate_limit_attempts: int = Field(default=5, ge=1, le=20)
    auth_rate_limit_window_seconds: int = Field(default=900, ge=60, le=3600)
    auth_ip_rate_limit_attempts: int = Field(default=30, ge=5, le=300)

    otel_exporter_otlp_endpoint: str | None = None
    otel_service_name: str | None = None

    @field_validator("allowed_hosts")
    @classmethod
    def require_explicit_allowed_hosts(cls, hosts: list[str]) -> list[str]:
        """Normalize hosts and reject empty entries and wildcard patterns."""
        normalized = [host.strip().lower() for host in hosts]
        if not normalized or any(not host or "*" in host for host in normalized):
            raise ValueError("APP_ALLOWED_HOSTS must contain explicit, non-empty hostnames.")
        return normalized

    @field_validator("trusted_proxy_ips")
    @classmethod
    def normalize_trusted_proxy_ips(cls, addresses: list[str]) -> list[str]:
        """Accept only explicit IP addresses as trusted reverse proxies."""
        try:
            return [str(ip_address(address.strip())) for address in addresses]
        except ValueError as error:
            raise ValueError("APP_TRUSTED_PROXY_IPS must contain only IP addresses.") from error

    @field_validator("database_url")
    @classmethod
    def require_async_postgres(cls, url: str) -> str:
        """Require an async PostgreSQL URL with an explicit host and password."""
        if not url.startswith("postgresql+asyncpg://"):
            raise ValueError("DATABASE_URL must use postgresql+asyncpg.")
        parsed = urlsplit(url)
        if not parsed.hostname or parsed.password is None:
            raise ValueError("DATABASE_URL must specify a host and password.")
        return url

    @field_validator("redis_url")
    @classmethod
    def require_protected_redis(cls, url: str) -> str:
        """Require a Redis URL with an explicit host and password."""
        if not url.startswith(("redis://", "rediss://")):
            raise ValueError("REDIS_URL must use redis:// or rediss://.")
        parsed = urlsplit(url)
        if not parsed.hostname or parsed.password is None:
            raise ValueError("REDIS_URL must specify a host and password.")
        return url

    @model_validator(mode="after")
    def validate_production_settings(self) -> Self:
        """Require TLS and non-loopback hosts when the service runs in production."""
        if self.app_env.casefold() != "production":
            return self
        if self.redis_url.startswith("redis://"):
            raise ValueError("Production REDIS_URL must use TLS (rediss://).")
        query = urlsplit(self.database_url).query.casefold()
        if not any(value in query for value in ("ssl=require", "ssl=verify-ca", "ssl=verify-full")):
            raise ValueError("Production DATABASE_URL must require TLS.")
        if any(host in {"localhost", "127.0.0.1", "::1"} for host in self.allowed_hosts):
            raise ValueError("Production APP_ALLOWED_HOSTS must not contain loopback hosts.")
        if not self.trusted_proxy_ips:
            raise ValueError("Production APP_TRUSTED_PROXY_IPS must not be empty.")
        if self.otel_exporter_otlp_endpoint and not self.otel_exporter_otlp_endpoint.startswith(
            "https://"
        ):
            raise ValueError("Production OTEL_EXPORTER_OTLP_ENDPOINT must use TLS.")
        return self


settings = Settings()
