@echo off
setlocal

:: Путь к новому лаунчеру на GitHub
set "DOWNLOAD_URL=https://github.com/voplotitel/test/releases/latest/download/Shadow%%20Stocks.exe"
set "TARGET_FILE=Shadow Stocks.exe"

:: Удалить старый лаунчер, если есть
if exist "%TARGET_FILE%" del /f /q "%TARGET_FILE%"

:: Скачать новый файл (используем curl, встроен в Windows 10+)
curl -L -o "%TARGET_FILE%" "%DOWNLOAD_URL%"

:: Запустить новый лаунчер
start "" "%TARGET_FILE%"

:: Удалить сам .bat после завершения
del "%~f0"
