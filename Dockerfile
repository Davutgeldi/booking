FROM python:3.12.13-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-install-project

COPY . .

RUN uv sync --frozen

#CMD ["uv", "run", "python", "src/main.py"]

CMD ["/bin/sh", "-c", "uv run alembic upgrade head && uv run python src/main.py"] 