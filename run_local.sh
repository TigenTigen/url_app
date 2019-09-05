#!/usr/bin/env bash

echo '\e[92m Проверка обновлений списка необходимых модулей:'
pip install -r requirements.txt

echo '\e[92m Сборка статических файлов:'
python3 django/manage.py collectstatic --noinput
echo '\e[92m Создание миграций:'
python3 django/manage.py makemigrations core
echo '\e[92m Применение миграций:'
python3 django/manage.py migrate

echo '\e[92m Запуск сервера:'
python3 django/manage.py run_server_and_start_worker
