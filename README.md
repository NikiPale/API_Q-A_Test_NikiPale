# API Сервис Вопросов и Ответов

RESTful API сервис для управления вопросами и ответами, построенный на FastAPI и PostgreSQL.

## Возможности

- Создание, чтение и удаление вопросов
- Добавление нескольких ответов к вопросам
- Каскадное удаление (удаление вопроса удаляет все его ответы)
- Валидация входных данных с помощью Pydantic
- База данных PostgreSQL с ORM SQLAlchemy
- Миграции базы данных с Alembic
- Комплексное логирование
- Unit-тесты с pytest
- Поддержка Docker и docker-compose
- API документация (Swagger/ReDoc)

## Технологический стек

- **FastAPI** - Современный веб-фреймворк для создания API
- **PostgreSQL** - Реляционная база данных
- **SQLAlchemy** - SQL инструментарий и ORM
- **Alembic** - Инструмент для миграций базы данных
- **Pydantic** - Валидация данных с использованием аннотаций типов Python
- **Docker** - Контейнеризация
- **pytest** - Фреймворк для тестирования

## Структура проекта

```
qa-api-service/
├── app/                    # Код приложения
│   ├── api/               # API endpoints
│   ├── models/            # Модели базы данных
│   ├── schemas/           # Pydantic схемы
│   └── utils/             # Утилиты (логирование и т.д.)
├── tests/                  # Файлы тестов
├── alembic/               # Миграции базы данных
├── docker-compose.yml     # Конфигурация Docker compose
├── Dockerfile             # Определение Docker образа
└── requirements.txt       # Python зависимости
```

## Быстрый старт

### Предварительные требования

- Docker и Docker Compose установлены
- Git

### Установка и запуск

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd qa-api-service
```

2. Создайте файл .env (необязательно, предоставлены значения по умолчанию):
```bash
cp .env.example .env
```

3. Запустите приложение:
```bash
docker-compose up
```

API будет доступно по адресу http://localhost:8000

### Документация API

После запуска приложения вы можете получить доступ к:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

**Примечание**: Интерфейс API документации и все сообщения об ошибках представлены на английском языке. Это обеспечивает максимальную совместимость с различными браузерами, системами мониторинга и инструментами разработки, а также соответствует международным стандартам REST API документирования.

## API Endpoints

### Вопросы

- GET /api/v1/questions/ - Получить все вопросы
- POST /api/v1/questions/ - Создать новый вопрос
- GET /api/v1/questions/{id} - Получить вопрос со всеми его ответами
- DELETE /api/v1/questions/{id} - Удалить вопрос (и его ответы)

### Ответы

- POST /api/v1/questions/{id}/answers/ - Добавить ответ к вопросу
- GET /api/v1/answers/{id} - Получить конкретный ответ
- DELETE /api/v1/answers/{id} - Удалить ответ

## Запуск тестов

### С Docker:
```bash
docker-compose exec api pytest tests/ -v
```

### Локально (требует Python окружение):
```bash
pip install -r requirements.txt
pytest tests/ -v
```

## Миграции базы данных

Миграции автоматически выполняются при запуске контейнера. Для создания новых миграций:

```bash
docker-compose exec api alembic revision --autogenerate -m "Описание"
docker-compose exec api alembic upgrade head
```

## Разработка

### Настройка локальной разработки

1. Создайте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Настройте PostgreSQL локально или используйте Docker:
```bash
docker run -d \
  --name postgres \
  -e POSTGRES_USER=user \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=qa_db \
  -p 5432:5432 \
  postgres:15-alpine
```

4. Выполните миграции:
```bash
alembic upgrade head
```

5. Запустите сервер разработки:
```bash
uvicorn app.main:app --reload
```

## Бизнес-логика

- **Валидация**: Все текстовые поля (вопросы и ответы) должны быть непустыми
- **ID пользователя**: Должен быть в корректном UUID формате
- **Каскадное удаление**: При удалении вопроса все связанные ответы автоматически удаляются
- **Множественные ответы**: Один пользователь может дать несколько ответов на один вопрос
- **Ссылочная целостность**: Нельзя создать ответ для несуществующего вопроса

## Обработка ошибок

API возвращает соответствующие HTTP статус коды:
- 200 OK - Успешные GET запросы
- 201 Created - Успешные POST запросы
- 204 No Content - Успешные DELETE запросы
- 404 Not Found - Ресурс не найден
- 422 Unprocessable Entity - Ошибки валидации

## Лицензия

MIT

## Автор

Niki Pale
