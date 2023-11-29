# Сайт на flask

Можно легко развернуть локально

### Способ 1 - Docker

скачиваете Docker

    # в корне
    docker compose build
    docker compose up

### Способ 2 - Python

    # в корне
    # виртуальное окружение
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    
    # база данных
    flask db migrate

    # запуск
    flask run