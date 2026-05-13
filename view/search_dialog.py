"""
Модуль диалога поиска записей с отображением результатов.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any

from controller import AppController


class SearchDialog:
    """
    Диалог поиска записей с отображением результатов в этом же окне.
    """

    def __init__(self, parent, controller: AppController):
        self.controller = controller
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Поиск записей")
        self.dialog.geometry("1100x650")
        self.dialog.minsize(900, 550)
        self.dialog.grab_set()
        self.dialog.transient(parent)

        # Переменные для условий поиска
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

        # Переменные для пагинации результатов
        self.current_page = 1
        self.records_per_page = 10
        self.search_results = []

        self._create_widgets()
        self._center_dialog(parent)

    def _create_widgets(self):
        """Создаёт все элементы диалога."""
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Левая панель - условия поиска
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        # Правая панель - результаты
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

        # ========== ЛЕВАЯ ПАНЕЛЬ: УСЛОВИЯ ПОИСКА ==========
        conditions_frame = ttk.LabelFrame(left_frame, text="Условия поиска", padding="10")
        conditions_frame.pack(fill=tk.BOTH, expand=True)

        # 1. По ФИО студента
        student_frame = ttk.LabelFrame(conditions_frame, text="По ФИО студента", padding="5")
        student_frame.pack(fill=tk.X, pady=5)

        cb_student = ttk.Checkbutton(
            student_frame, text="Использовать", variable=self.use_student_fio
        )
        cb_student.grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=2)

        ttk.Label(student_frame, text="Значение (любая часть ФИО):").grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Entry(student_frame, textvariable=self.student_fio_value, width=35).grid(row=1, column=1, padx=5)

        ttk.Checkbutton(
            student_frame, text="Учитывать регистр", variable=self.student_case_sensitive
        ).grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=2)

        # 2. По ФИО родителя
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
        ttk.Entry(parent_frame, textvariable=self.parent_fio_value, width=35).grid(row=2, column=1, padx=5)

        ttk.Checkbutton(
            parent_frame, text="Учитывать регистр", variable=self.parent_case_sensitive
        ).grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=2)

        # 3. По числу братьев/сестер
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

        # 4. По доходу родителя
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

        # Кнопки управления поиском
        search_button_frame = ttk.Frame(conditions_frame)
        search_button_frame.pack(fill=tk.X, pady=10)

        ttk.Button(search_button_frame, text="Найти", command=self._on_search).pack(side=tk.LEFT, padx=5)
        ttk.Button(search_button_frame, text="Очистить", command=self._on_clear).pack(side=tk.LEFT, padx=5)
        ttk.Button(search_button_frame, text="Закрыть", command=self._on_close).pack(side=tk.RIGHT, padx=5)

        # ========== ПРАВАЯ ПАНЕЛЬ: РЕЗУЛЬТАТЫ ПОИСКА ==========
        results_frame = ttk.LabelFrame(right_frame, text="Результаты поиска", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True)

        # Таблица результатов
        columns = ("№", "ФИО студента", "ФИО отца", "Доход отца", "ФИО матери", "Доход матери", "Братья", "Сёстры")

        result_tree_frame = ttk.Frame(results_frame)
        result_tree_frame.pack(fill=tk.BOTH, expand=True)

        scroll_y = ttk.Scrollbar(result_tree_frame, orient=tk.VERTICAL)
        scroll_x = ttk.Scrollbar(result_tree_frame, orient=tk.HORIZONTAL)

        self.result_tree = ttk.Treeview(
            result_tree_frame,
            columns=columns,
            show="headings",
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
            height=12
        )

        scroll_y.config(command=self.result_tree.yview)
        scroll_x.config(command=self.result_tree.xview)

        column_widths = [40, 200, 160, 100, 160, 100, 70, 70]
        for col, width in zip(columns, column_widths):
            self.result_tree.heading(col, text=col)
            self.result_tree.column(col, width=width, minwidth=width)

        self.result_tree.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")

        result_tree_frame.grid_rowconfigure(0, weight=1)
        result_tree_frame.grid_columnconfigure(0, weight=1)

        # Панель пагинации результатов
        pagination_frame = ttk.Frame(results_frame)
        pagination_frame.pack(fill=tk.X, pady=5)

        self.btn_first = ttk.Button(pagination_frame, text="<<", command=self._first_page, width=5)
        self.btn_first.pack(side=tk.LEFT, padx=2)

        self.btn_prev = ttk.Button(pagination_frame, text="<", command=self._prev_page, width=5)
        self.btn_prev.pack(side=tk.LEFT, padx=2)

        self.lbl_page = ttk.Label(pagination_frame, text="Страница: 0 из 0")
        self.lbl_page.pack(side=tk.LEFT, padx=10)

        self.btn_next = ttk.Button(pagination_frame, text=">", command=self._next_page, width=5)
        self.btn_next.pack(side=tk.LEFT, padx=2)

        self.btn_last = ttk.Button(pagination_frame, text=">>", command=self._last_page, width=5)
        self.btn_last.pack(side=tk.LEFT, padx=2)

        self.lbl_found = ttk.Label(pagination_frame, text="Всего найдено: 0")
        self.lbl_found.pack(side=tk.RIGHT, padx=10)

    def _center_dialog(self, parent):
        self.dialog.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - self.dialog.winfo_width()) // 2
        y = parent.winfo_y() + (parent.winfo_height() - self.dialog.winfo_height()) // 2
        self.dialog.geometry(f"+{x}+{y}")

    def _build_criteria(self) -> Dict[str, Any]:
        """Собирает критерии поиска из активных условий."""
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

    def _display_results(self):
        """Отображает текущую страницу результатов."""
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)

        start = (self.current_page - 1) * self.records_per_page
        end = start + self.records_per_page
        page_records = self.search_results[start:end]

        for i, record in enumerate(page_records):
            student_fio = " ".join(filter(None, [
                record.student_lastname, record.student_firstname, record.student_patronymic
            ])) or "—"

            father_fio = " ".join(filter(None, [
                record.father_lastname, record.father_firstname, record.father_patronymic
            ])) or "—"

            mother_fio = " ".join(filter(None, [
                record.mother_lastname, record.mother_firstname, record.mother_patronymic
            ])) or "—"

            father_income = f"{record.father_income:,.0f}" if record.father_income > 0 else "0"
            mother_income = f"{record.mother_income:,.0f}" if record.mother_income > 0 else "0"

            self.result_tree.insert("", tk.END, values=(
                start + i + 1,
                student_fio,
                father_fio,
                father_income,
                mother_fio,
                mother_income,
                record.brothers_count,
                record.sisters_count
            ))

        # Обновляем информацию о пагинации
        total_pages = max(1, (len(self.search_results) + self.records_per_page - 1) // self.records_per_page)
        self.lbl_page.config(text=f"Страница: {self.current_page} из {total_pages}")
        self.lbl_found.config(text=f"Всего найдено: {len(self.search_results)}")

        self.btn_first.config(state=tk.NORMAL if self.current_page > 1 else tk.DISABLED)
        self.btn_prev.config(state=tk.NORMAL if self.current_page > 1 else tk.DISABLED)
        self.btn_next.config(state=tk.NORMAL if self.current_page < total_pages else tk.DISABLED)
        self.btn_last.config(state=tk.NORMAL if self.current_page < total_pages else tk.DISABLED)

    def _on_search(self):
        """Выполняет поиск по активным условиям."""
        criteria = self._build_criteria()

        if not criteria:
            messagebox.showwarning(
                "Внимание",
                "Не выбрано ни одного условия поиска.\nПоставьте галочку 'Использовать' у нужного условия и заполните его.",
                parent=self.dialog
            )
            return

        self.search_results = self.controller.search_records(criteria)
        self.current_page = 1
        self._display_results()

        if not self.search_results:
            messagebox.showinfo(
                "Результаты поиска",
                "Записи, соответствующие условиям, не найдены",
                parent=self.dialog
            )

    def _on_clear(self):
        """Очищает все поля ввода и результаты."""
        self.use_student_fio.set(False)
        self.student_fio_value.set("")
        self.student_case_sensitive.set(False)

        self.use_parent_fio.set(False)
        self.parent_fio_value.set("")
        self.parent_case_sensitive.set(False)

        self.use_siblings.set(False)
        self.siblings_count.set("")

        self.use_income.set(False)
        self.income_min.set("")
        self.income_max.set("")

        for item in self.result_tree.get_children():
            self.result_tree.delete(item)

        self.search_results = []
        self.lbl_page.config(text="Страница: 0 из 0")
        self.lbl_found.config(text="Всего найдено: 0")

    def _first_page(self):
        self.current_page = 1
        self._display_results()

    def _prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self._display_results()

    def _next_page(self):
        total_pages = max(1, (len(self.search_results) + self.records_per_page - 1) // self.records_per_page)
        if self.current_page < total_pages:
            self.current_page += 1
            self._display_results()

    def _last_page(self):
        total_pages = max(1, (len(self.search_results) + self.records_per_page - 1) // self.records_per_page)
        self.current_page = total_pages
        self._display_results()

    def _on_close(self):
        self.dialog.destroy()