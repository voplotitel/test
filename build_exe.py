import PyInstaller.__main__
import os

# Путь к основному файлу игры
script_path = os.path.join('src', 'main.py')

# Запуск PyInstaller
PyInstaller.__main__.run([
    script_path,
    '--name=ShadowStocks',
    '--onefile',
    '--windowed',
    '--icon=assets/icon.ico' if os.path.exists('assets/icon.ico') else None,
    '--add-data=assets;assets' if os.path.exists('assets') else None,
    '--clean',
]) 