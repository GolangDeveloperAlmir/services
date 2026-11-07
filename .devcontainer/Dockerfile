FROM mcr.microsoft.com/devcontainers/python:1-3.14-bookworm

COPY --from=ghcr.io/astral-sh/uv:0.6.5 /uv /uvx /bin/

ENV UV_LINK_MODE=copy

WORKDIR /workspace
