# Заглушка Dockerfile для Django
FROM python:3.10-slim

WORKDIR /app

# Устанавливаем зависимости (здесь пока пустой файл)
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY . /app/

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
