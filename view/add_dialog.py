"""
Модуль диалога добавления новой записи.
"""

import tkinter as tk
from tkinter import ttk, messagebox

from model.student_record import StudentRecord
from controller import AppController


class AddDialog:
    """
    Диалог добавления новой записи о студенте и его семье.
    """

    def __init__(self, parent, controller: AppController):
        self.controller = controller
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Добавление записи")
        self.dialog.geometry("500x600")
        self.dialog.resizable(False, False)
        self.dialog.grab_set()
        self.dialog.transient(parent)

        self._create_widgets()
        self._center_dialog(parent)

    def _create_widgets(self):
        """Создаёт все элементы диалога."""
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Студент
        student_frame = ttk.LabelFrame(main_frame, text="Студент", padding="10")
        student_frame.pack(fill=tk.X, pady=5)

        ttk.Label(student_frame, text="Фамилия:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.student_lastname_entry = ttk.Entry(student_frame, width=30)
        self.student_lastname_entry.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(student_frame, text="Имя:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.student_firstname_entry = ttk.Entry(student_frame, width=30)
        self.student_firstname_entry.grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(student_frame, text="Отчество:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        self.student_patronymic_entry = ttk.Entry(student_frame, width=30)
        self.student_patronymic_entry.grid(row=2, column=1, padx=5, pady=2)

        # Отец
        father_frame = ttk.LabelFrame(main_frame, text="Отец", padding="10")
        father_frame.pack(fill=tk.X, pady=5)

        ttk.Label(father_frame, text="Фамилия:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.father_lastname_entry = ttk.Entry(father_frame, width=30)
        self.father_lastname_entry.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(father_frame, text="Имя:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.father_firstname_entry = ttk.Entry(father_frame, width=30)
        self.father_firstname_entry.grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(father_frame, text="Отчество:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        self.father_patronymic_entry = ttk.Entry(father_frame, width=30)
        self.father_patronymic_entry.grid(row=2, column=1, padx=5, pady=2)

        ttk.Label(father_frame, text="Заработок (руб.):").grid(row=3, column=0, sticky=tk.W, padx=5, pady=2)
        self.father_income_entry = ttk.Entry(father_frame, width=30)
        self.father_income_entry.grid(row=3, column=1, padx=5, pady=2)

        # Мать
        mother_frame = ttk.LabelFrame(main_frame, text="Мать", padding="10")
        mother_frame.pack(fill=tk.X, pady=5)

        ttk.Label(mother_frame, text="Фамилия:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.mother_lastname_entry = ttk.Entry(mother_frame, width=30)
        self.mother_lastname_entry.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(mother_frame, text="Имя:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.mother_firstname_entry = ttk.Entry(mother_frame, width=30)
        self.mother_firstname_entry.grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(mother_frame, text="Отчество:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        self.mother_patronymic_entry = ttk.Entry(mother_frame, width=30)
        self.mother_patronymic_entry.grid(row=2, column=1, padx=5, pady=2)

        ttk.Label(mother_frame, text="Заработок (руб.):").grid(row=3, column=0, sticky=tk.W, padx=5, pady=2)
        self.mother_income_entry = ttk.Entry(mother_frame, width=30)
        self.mother_income_entry.grid(row=3, column=1, padx=5, pady=2)

        # Состав семьи
        siblings_frame = ttk.LabelFrame(main_frame, text="Состав семьи", padding="10")
        siblings_frame.pack(fill=tk.X, pady=5)

        ttk.Label(siblings_frame, text="Число братьев:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.brothers_spinbox = ttk.Spinbox(siblings_frame, from_=0, to=20, width=10)
        self.brothers_spinbox.grid(row=0, column=1, padx=5, pady=2, sticky=tk.W)
        self.brothers_spinbox.set(0)

        ttk.Label(siblings_frame, text="Число сестёр:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.sisters_spinbox = ttk.Spinbox(siblings_frame, from_=0, to=20, width=10)
        self.sisters_spinbox.grid(row=1, column=1, padx=5, pady=2, sticky=tk.W)
        self.sisters_spinbox.set(0)

        # Кнопки
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=15)

        ok_btn = ttk.Button(button_frame, text="Добавить", command=self._on_ok)
        ok_btn.pack(side=tk.RIGHT, padx=5)

        cancel_btn = ttk.Button(button_frame, text="Отмена", command=self._on_cancel)
        cancel_btn.pack(side=tk.RIGHT, padx=5)

    def _center_dialog(self, parent):
        self.dialog.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - self.dialog.winfo_width()) // 2
        y = parent.winfo_y() + (parent.winfo_height() - self.dialog.winfo_height()) // 2
        self.dialog.geometry(f"+{x}+{y}")

    def _get_values(self):
        return {
            "student_lastname": self.student_lastname_entry.get(),
            "student_firstname": self.student_firstname_entry.get(),
            "student_patronymic": self.student_patronymic_entry.get(),
            "father_lastname": self.father_lastname_entry.get(),
            "father_firstname": self.father_firstname_entry.get(),
            "father_patronymic": self.father_patronymic_entry.get(),
            "father_income": self.father_income_entry.get(),
            "mother_lastname": self.mother_lastname_entry.get(),
            "mother_firstname": self.mother_firstname_entry.get(),
            "mother_patronymic": self.mother_patronymic_entry.get(),
            "mother_income": self.mother_income_entry.get(),
            "brothers_count": self.brothers_spinbox.get(),
            "sisters_count": self.sisters_spinbox.get()
        }

    def _on_ok(self):
        try:
            values = self._get_values()

            father_income = float(values["father_income"]) if values["father_income"] else 0.0
            mother_income = float(values["mother_income"]) if values["mother_income"] else 0.0
            brothers = int(values["brothers_count"]) if values["brothers_count"] else 0
            sisters = int(values["sisters_count"]) if values["sisters_count"] else 0

            record = StudentRecord(
                student_lastname=values["student_lastname"],
                student_firstname=values["student_firstname"],
                student_patronymic=values["student_patronymic"],
                father_lastname=values["father_lastname"],
                father_firstname=values["father_firstname"],
                father_patronymic=values["father_patronymic"],
                father_income=father_income,
                mother_lastname=values["mother_lastname"],
                mother_firstname=values["mother_firstname"],
                mother_patronymic=values["mother_patronymic"],
                mother_income=mother_income,
                brothers_count=brothers,
                sisters_count=sisters
            )

            is_valid, error_msg = record.validate()
            if not is_valid:
                messagebox.showerror("Ошибка валидации", error_msg, parent=self.dialog)
                return

            if self.controller.add_record(record):
                messagebox.showinfo("Успех", "Запись успешно добавлена", parent=self.dialog)
                self.dialog.destroy()
            else:
                messagebox.showerror("Ошибка", "Не удалось добавить запись", parent=self.dialog)

        except ValueError as e:
            messagebox.showerror("Ошибка ввода", f"Неверный формат числа: {e}", parent=self.dialog)

    def _on_cancel(self):
        self.dialog.destroy()