@echo off
chcp 65001 >nul

if not exist env (
    echo Creating virtual environment... [Please wait]
    py -m venv env
)

echo Activating virtual environment... [Please wait]
call env\Scripts\activate

echo Installing dependencies... [Please wait]
pip install -r requirements.txt

echo Applying migrations... [Please wait]
py manage.py makemigrations accounts
py manage.py migrate


echo Starting Django server... Open the link [SUCCESS]
py manage.py runserver

pause
