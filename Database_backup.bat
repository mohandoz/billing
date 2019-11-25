@echo off
cmd /k "cd /d d:\venv\scripts & activate & cd /d d:\billing & python manage.py dbbackup"