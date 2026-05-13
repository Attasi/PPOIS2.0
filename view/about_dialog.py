"""
Модуль диалога "О программе".
"""

import tkinter as tk
from tkinter import ttk


class AboutDialog:
    """
    Диалог с информацией о программе.
    """

    def __init__(self, parent):
        """
        Инициализация диалога "О программе".

        Args:
            parent: Родительское окно
        """
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("О программе")
        self.dialog.geometry("400x250")
        self.dialog.resizable(False, False)
        self.dialog.grab_set()

        self._create_widgets()
        self._center_dialog(parent)

    def _create_widgets(self) -> None:
        """Создаёт все элементы диалога."""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Название программы
        title_label = ttk.Label(
            main_frame,
            text="Учёт семей студентов",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)

        # Версия
        version_label = ttk.Label(
            main_frame,
            text="Версия 1.0",
            font=("Arial", 10)
        )
        version_label.pack()

        # Разделитель
        ttk.Separator(main_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=15)

        # Описание
        desc_text = (
            "Программа для учёта информации о студентах и их семьях.\n\n"
            "Возможности:\n"
            "• Добавление, поиск и удаление записей\n"
            "• Поиск по ФИО студента, ФИО родителя,\n"
            "  количеству братьев/сестер, доходу родителей\n"
            "• Сохранение и загрузка данных в XML\n"
            "• Постраничный вывод записей"
        )

        desc_label = ttk.Label(main_frame, text=desc_text, justify=tk.LEFT)
        desc_label.pack(pady=10)

        # Разделитель
        ttk.Separator(main_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)

        # Кнопка OK
        ttk.Button(main_frame, text="OK", command=self.dialog.destroy).pack(pady=5)

    def _center_dialog(self, parent) -> None:
        """Центрирует диалог относительно родительского окна."""
        self.dialog.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - self.dialog.winfo_width()) // 2
        y = parent.winfo_y() + (parent.winfo_height() - self.dialog.winfo_height()) // 2
        self.dialog.geometry(f"+{x}+{y}")