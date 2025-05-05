import os
import sys

# Добавляем путь к src в PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Импортируем и запускаем игру
from main import Game

if __name__ == "__main__":
    game = Game()
    game.run() 