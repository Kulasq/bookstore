FROM python:3.13-slim AS python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# Instalar dependências do sistema
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    curl \
    build-essential \
    libpq-dev \
    gcc && \
    rm -rf /var/lib/apt/lists/*

# Instalar Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    poetry --version

# Configurar diretório de trabalho para instalação
WORKDIR $PYSETUP_PATH

# Copiar arquivos de dependências
COPY pyproject.toml poetry.lock* ./

# Instalar dependências
RUN poetry install --no-root --without dev

# Configurar diretório da aplicação
WORKDIR /app

# Copiar código da aplicação
COPY . /app/

# Expor porta
EXPOSE 8000

# Comando para executar a aplicação
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]