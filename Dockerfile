# python-base define variáveis e ambiente compartilhado
FROM python:3.13-slim AS python-base

# ---- ENV comuns ----
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=2.1.4 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

# poetry e .venv no PATH
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# deps do sistema
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
       curl \
       build-essential \
    && rm -rf /var/lib/apt/lists/*

# instala Poetry (fixado na versão acima)
RUN pip install "poetry==$POETRY_VERSION"

# ----------------- Fase: deps Python -----------------
WORKDIR $PYSETUP_PATH

# copie METADADOS do projeto para permitir cache de layer
# (inclui o README pois o [project] readme aponta para ele)
COPY pyproject.toml poetry.lock* README.md ./

# instala dependências no .venv do projeto
# (sem instalar o próprio projeto – como é um app, não precisa)
RUN poetry install --no-root

# ----------------- Fase: app -----------------
WORKDIR /app
COPY . /app/

EXPOSE 8000

# usa o Python do .venv criado pelo Poetry (está no PATH)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
