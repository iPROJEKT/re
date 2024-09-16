FROM python:3.12-alpine

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /re

# Устанавливаем системные зависимости
RUN apk add --no-cache gcc musl-dev libffi-dev

# Копируем файл requirements.txt в контейнер
COPY requirements.txt .

# Устанавливаем зависимости из requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в рабочую директорию контейнера
COPY . .

# Настраиваем переменные окружения
ENV PYTHONUNBUFFERED=1

# Прогоняем миграции перед запуском бота
EXPOSE 8000

# Команда для запуска FastAPI приложения
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]