### Кошачий благотворительный фонд (0.1.0)

API для благотворительного фонда помощи животным. 
Создано с применением Python, FastAPI, SQLAlchemy, Pydantic.
Предусмотрена аутентификация пользователей(JWT).
Приложение позволяет создавать проекты и делать пожертвования.
Спецификация API описана в файле openapi.json

## Как установить программу

Клонировать репозиторий и перейти в него в командной строке:

```
git clone 
```

```
cd yacut
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Создать миграции

```
alembic revision --autogenerate
```
```
alembic upgrade head
```

Запустить программу:

```
uvicorn app.main:app -- reload
```
