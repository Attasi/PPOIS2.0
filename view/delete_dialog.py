"""
Модуль диалога удаления записей по условиям.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any

from controller import AppController


class DeleteDialog:
    """
    Диалог удаления записей по задан условиям.
    """

    def __init__(self, parent, controller: AppController):
        self.controller = controller
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Удаление записей")
        self.dialog.geometry("550x650")
        self.dialog.resizable(False, False)
        self.dialog.grab_set()
        self.dialog.transient(parent)

        # Переменные
        self.use_student_fio = tk.BooleanVar(value=False)
        self.student_fio_value = tk.StringVar()
        self.student_case_sensitive = tk.BooleanVar(value=False)

        self.use_parent_fio = tk.BooleanVar(value=False)
        self.parent_type = tk.StringVar(value="father")
        self.parent_fio_value = tk.StringVar()
        self.parent_case_sensitive = tk.BooleanVar(value=False)

        self.use_siblings = tk.BooleanVar(value=False)
        self.siblings_type = tk.StringVar(value="brothers")
        self.siblings_count = tk.StringVar()

        self.use_income = tk.BooleanVar(value=False)
        self.income_parent_type = tk.StringVar(value="father")
        self.income_min = tk.StringVar()
        self.income_max = tk.StringVar()

        self._create_widgets()
        self._center_dialog(parent)

    def _create_widgets(self):
        """Создаёт все элементы диалога."""
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        conditions_frame = ttk.LabelFrame(main_frame, text="Условия удаления", padding="10")
        conditions_frame.pack(fill=tk.BOTH, expand=True)

        # ===== По ФИО студента =====
        student_frame = ttk.LabelFrame(conditions_frame, text="По ФИО студента", padding="5")
        student_frame.pack(fill=tk.X, pady=5)

        cb_student = ttk.Checkbutton(
            student_frame, text="Использовать", variable=self.use_student_fio
        )
        cb_student.grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=2)

        ttk.Label(student_frame, text="Значение (любая часть ФИО):").grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Entry(student_frame, textvariable=self.student_fio_value, width=40).grid(row=1, column=1, padx=5)

        ttk.Checkbutton(
            student_frame, text="Учитывать регистр", variable=self.student_case_sensitive
        ).grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=2)

        # ===== По ФИО родителя =====
        parent_frame = ttk.LabelFrame(conditions_frame, text="По ФИО родителя", padding="5")
        parent_frame.pack(fill=tk.X, pady=5)

        cb_parent = ttk.Checkbutton(
            parent_frame, text="Использовать", variable=self.use_parent_fio
        )
        cb_parent.grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=2)

        ttk.Label(parent_frame, text="Родитель:").grid(row=1, column=0, sticky=tk.W, pady=2)
        parent_combo = ttk.Combobox(
            parent_frame, textvariable=self.parent_type,
            values=["father", "mother"], state="readonly", width=15
        )
        parent_combo.grid(row=1, column=1, padx=5, sticky=tk.W)

        ttk.Label(parent_frame, text="Значение (любая часть ФИО):").grid(row=2, column=0, sticky=tk.W, pady=2)
        ttk.Entry(parent_frame, textvariable=self.parent_fio_value, width=40).grid(row=2, column=1, padx=5)

        ttk.Checkbutton(
            parent_frame, text="Учитывать регистр", variable=self.parent_case_sensitive
        ).grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=2)

        # ===== По числу братьев/сестер =====
        siblings_frame = ttk.LabelFrame(conditions_frame, text="По числу братьев/сестер", padding="5")
        siblings_frame.pack(fill=tk.X, pady=5)

        cb_siblings = ttk.Checkbutton(
            siblings_frame, text="Использовать", variable=self.use_siblings
        )
        cb_siblings.grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=2)

        ttk.Label(siblings_frame, text="Тип:").grid(row=1, column=0, sticky=tk.W, pady=2)
        siblings_combo = ttk.Combobox(
            siblings_frame, textvariable=self.siblings_type,
            values=["brothers", "sisters"], state="readonly", width=15
        )
        siblings_combo.grid(row=1, column=1, padx=5, sticky=tk.W)

        ttk.Label(siblings_frame, text="Количество:").grid(row=2, column=0, sticky=tk.W, pady=2)
        ttk.Spinbox(siblings_frame, from_=0, to=20, textvariable=self.siblings_count, width=10).grid(
            row=2, column=1, padx=5, sticky=tk.W
        )

        # ===== По доходу родителя (ПОЛНОСТЬЮ ИСПРАВЛЕНО) =====
        income_frame = ttk.LabelFrame(conditions_frame, text="По доходу родителя", padding="5")
        income_frame.pack(fill=tk.X, pady=5)

        cb_income = ttk.Checkbutton(
            income_frame, text="Использовать", variable=self.use_income
        )
        cb_income.grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=2)

        ttk.Label(income_frame, text="Родитель:").grid(row=1, column=0, sticky=tk.W, pady=2)
        income_parent_combo = ttk.Combobox(
            income_frame, textvariable=self.income_parent_type,
            values=["father", "mother"], state="readonly", width=15
        )
        income_parent_combo.grid(row=1, column=1, padx=5, sticky=tk.W)

        ttk.Label(income_frame, text="Доход от (руб.):").grid(row=2, column=0, sticky=tk.W, pady=2)
        ttk.Entry(income_frame, textvariable=self.income_min, width=15).grid(row=2, column=1, padx=5, sticky=tk.W)

        ttk.Label(income_frame, text="Доход до (руб.):").grid(row=3, column=0, sticky=tk.W, pady=2)
        ttk.Entry(income_frame, textvariable=self.income_max, width=15).grid(row=3, column=1, padx=5, sticky=tk.W)

        # ===== КНОПКИ =====
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=15)

        delete_btn = ttk.Button(button_frame, text="Удалить", command=self._on_delete)
        delete_btn.pack(side=tk.RIGHT, padx=5)

        cancel_btn = ttk.Button(button_frame, text="Отмена", command=self._on_cancel)
        cancel_btn.pack(side=tk.RIGHT, padx=5)

    def _center_dialog(self, parent):
        self.dialog.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - self.dialog.winfo_width()) // 2
        y = parent.winfo_y() + (parent.winfo_height() - self.dialog.winfo_height()) // 2
        self.dialog.geometry(f"+{x}+{y}")

    def _build_criteria(self) -> Dict[str, Any]:
        criteria = {}

        if self.use_student_fio.get() and self.student_fio_value.get():
            criteria["student_fio"] = {
                "value": self.student_fio_value.get(),
                "case_sensitive": self.student_case_sensitive.get()
            }

        if self.use_parent_fio.get() and self.parent_fio_value.get():
            criteria["parent_fio"] = {
                "type": self.parent_type.get(),
                "value": self.parent_fio_value.get(),
                "case_sensitive": self.parent_case_sensitive.get()
            }

        if self.use_siblings.get() and self.siblings_count.get():
            try:
                criteria["siblings"] = {
                    "type": self.siblings_type.get(),
                    "count": int(self.siblings_count.get())
                }
            except ValueError:
                pass

        if self.use_income.get():
            income_criteria = {"type": self.income_parent_type.get()}
            if self.income_min.get():
                income_criteria["min"] = float(self.income_min.get())
            if self.income_max.get():
                income_criteria["max"] = float(self.income_max.get())
            if income_criteria.get("min") is not None or income_criteria.get("max") is not None:
                criteria["income"] = income_criteria

        return criteria

    def _on_delete(self):
        criteria = self._build_criteria()

        if not criteria:
            messagebox.showwarning("Внимание", "Заполните хотя бы одно условие удаления", parent=self.dialog)
            return

        if not messagebox.askyesno(
            "Подтверждение удаления",
            "Вы уверены, что хотите удалить записи, соответствующие указанным условиям?",
            parent=self.dialog
        ):
            return

        deleted_count = self.controller.delete_records(criteria)

        if deleted_count > 0:
            messagebox.showinfo(
                "Результат удаления",
                f"Удалено записей: {deleted_count}",
                parent=self.dialog
            )
            self.dialog.destroy()
        else:
            messagebox.showinfo(
                "Результат удаления",
                "Записи, соответствующие условиям, не найдены",
                parent=self.dialog
            )

    def _on_cancel(self):
        self.dialog.destroy()