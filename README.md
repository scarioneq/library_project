Инструкция по запуску приложения:
1. Склонировать
git clone https://github.com/scarioneq/library_project.git

2. Перейти в директорию проекта
cd library_project

3.Активировать виртуальное окружение
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

4.Установить зависимости
pip install -r requirements.txt

5. Настройка БД
python manage.py makemigrations
python manage.py migrate

6. Создание супер юзера
python manage.py createsuperuser

7. Запуск сервера
python manage.py runserver

