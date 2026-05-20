"""
Главный модуль запуска приложения "Учёт семей студентов".
"""

import sys
import os

# Добавляем корневую директорию в путь поиска модулей
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from controller import AppController
from view import MainWindow


def main():
    """
    Главная функция запуска приложения.
    """
    # Создаём контроллер
    controller = AppController()

    # Создаём и запускаем главное окно
    app = MainWindow(controller)
    app.run()


if __name__ == "__main__":
    main()