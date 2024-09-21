# Используем официальный образ Python
FROM python:3.12-slim

# Установим рабочую директорию
WORKDIR /app

# Установим системные зависимости для работы с PostgreSQL
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Копируем файл зависимостей (requirements.txt) в контейнер
COPY requirements.txt /app/

# Установим зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем оставшиеся файлы проекта в контейнер
COPY . /app/

# Применим миграции и запустим сервер Django
CMD ["bash", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
