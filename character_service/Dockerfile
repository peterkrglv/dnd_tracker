FROM python:3.12-slim

ENV POETRY_VERSION=1.8.3 \
    POETRY_HOME="/opt/poetry" \
    # Добавляем настройку для хранения venv вне проекта
    POETRY_VIRTUALENVS_IN_PROJECT=false \
    # Указываем, где будет храниться исполняемый файл uvicorn
    PATH="$POETRY_HOME/bin:$PATH"

RUN pip install --no-cache-dir poetry==$POETRY_VERSION

WORKDIR /app

# Копируем только файлы для установки зависимостей
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости. Venv теперь будет где-то в кеше Docker, а не в /app.
RUN poetry install --no-root --no-dev

# В режиме разработки (с монтированием) это не обязательно,
# но если оставить, это не повредит, так как volume перезапишет.
# COPY . .

# Согласуй порт с docker-compose.yml (8002)
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]