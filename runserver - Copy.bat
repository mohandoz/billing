d:\venv\scripts\activate

@echo off
setlocal
set ALLOWED_HOSTS=['localhost', '127.0.0.1']
set DJANGO_SETTINGS_MODULE=config.settings.production
set DJANGO_SECRET_KEY=dwqkjd@OKR@!_12/f021ir021fsav1_21rflkm
set DATABASE_URL=postgres://billing:Amman123@localhost:5432/billing
set DJANGO_ADMIN_URL=MohandozAdmin

setx PATH "%DJANGO_SETTINGS_MODULE%%DJANGO_SECRET_KEY%%DATABASE_URL%%DJANGO_ADMIN_URL%" /m

endlocal
python manage.py runserver


setx ALLOWED_HOSTS "['localhost', '127.0.0.1']"
setx DJANGO_SETTINGS_MODULE config.settings.production
setx DJANGO_SECRET_KEY dwqkjd@OKR@!_12/f021ir021fsav1_21rflkm
setx DATABASE_URL postgres://billing:Amman123@localhost:5432/billing
setx DJANGO_ADMIN_URL MohandozAdmin