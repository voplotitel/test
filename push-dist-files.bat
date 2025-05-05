@echo off
cd /d %~dp0

:: Получаем дату в формате ГГГГ-ММ-ДД
for /f %%i in ('powershell -command "Get-Date -Format yyyy-MM-dd"') do set DATE=%%i

:: Читаем версию из файла version.txt
set /p VERSION=<dist\version.txt

:: Формируем сообщение коммита
set MESSAGE=Обновление лаунчера %VERSION% от %DATE%

echo Добавление файлов из dist...
git add -f dist\game.exe dist\config.json dist\version.txt

echo Создание коммита: %MESSAGE%
git commit -m "%MESSAGE%"

echo Отправка на GitHub...
git push origin main

echo Готово!
pause