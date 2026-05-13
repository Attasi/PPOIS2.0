"""
Модуль главного окна приложения "Учёт семей студентов".
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from controller import AppController
from view.add_dialog import AddDialog
from view.search_dialog import SearchDialog
from view.delete_dialog import DeleteDialog
from view.about_dialog import AboutDialog


class MainWindow:
    """
    Главное окно приложения.
    """

    def __init__(self, controller: AppController):
        self.controller = controller
        self.root = tk.Tk()
        self.root.title("Учёт семей студентов")
        self.root.geometry("1300x650")
        self.root.minsize(1100, 550)

        self.records_per_page_var = tk.StringVar(value="10")
        self.page_info_var = tk.StringVar(value="Страница: 1 из 1")
        self.total_records_var = tk.StringVar(value="Всего записей: 0")

        self._create_menu()
        self._create_toolbar()
        self._create_table()
        self._create_pagination()
        self._create_statusbar()

        self._refresh_table()

        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Загрузить", command=self._load_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Сохранить", command=self._save_file, accelerator="Ctrl+S")
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self._on_closing, accelerator="Ctrl+Q")

        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Правка", menu=edit_menu)
        edit_menu.add_command(label="Добавить", command=self._show_add_dialog, accelerator="Ctrl+A")
        edit_menu.add_command(label="Поиск", command=self._show_search_dialog, accelerator="Ctrl+F")
        edit_menu.add_command(label="Удалить", command=self._show_delete_dialog, accelerator="Ctrl+D")

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Справка", menu=help_menu)
        help_menu.add_command(label="О программе", command=self._show_about_dialog)

        self.root.bind("<Control-o>", lambda e: self._load_file())
        self.root.bind("<Control-s>", lambda e: self._save_file())
        self.root.bind("<Control-a>", lambda e: self._show_add_dialog())
        self.root.bind("<Control-f>", lambda e: self._show_search_dialog())
        self.root.bind("<Control-d>", lambda e: self._show_delete_dialog())
        self.root.bind("<Control-q>", lambda e: self._on_closing())

    def _create_toolbar(self):
        toolbar = ttk.Frame(self.root)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        buttons = [
            ("Добавить", self._show_add_dialog),
            ("Поиск", self._show_search_dialog),
            ("Удалить", self._show_delete_dialog),
            ("Загрузить", self._load_file),
            ("Сохранить", self._save_file)
        ]

        for text, command in buttons:
            btn = ttk.Button(toolbar, text=text, command=command)
            btn.pack(side=tk.LEFT, padx=2)

    def _create_table(self):
        table_frame = ttk.Frame(self.root)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        scroll_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)
        scroll_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)

        columns = (
            "№",
            "ФИО студента",
            "ФИО отца",
            "заработок отца",
            "ФИО матери",
            "заработок матери",
            "Число братьев",
            "Число сестер"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
            height=15
        )

        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)

        column_widths = [40, 220, 180, 100, 180, 100, 80, 80]
        for col, width in zip(columns, column_widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, minwidth=width)

        self.tree.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

    def _create_pagination(self):
        pagination_frame = ttk.Frame(self.root)
        pagination_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)

        self.btn_first = ttk.Button(pagination_frame, text="<<", command=self._first_page, width=5)
        self.btn_first.pack(side=tk.LEFT, padx=2)

        self.btn_prev = ttk.Button(pagination_frame, text="<", command=self._prev_page, width=5)
        self.btn_prev.pack(side=tk.LEFT, padx=2)

        self.lbl_page = ttk.Label(pagination_frame, textvariable=self.page_info_var)
        self.lbl_page.pack(side=tk.LEFT, padx=10)

        self.btn_next = ttk.Button(pagination_frame, text=">", command=self._next_page, width=5)
        self.btn_next.pack(side=tk.LEFT, padx=2)

        self.btn_last = ttk.Button(pagination_frame, text=">>", command=self._last_page, width=5)
        self.btn_last.pack(side=tk.LEFT, padx=2)

        ttk.Separator(pagination_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)

        ttk.Label(pagination_frame, text="Записей на странице:").pack(side=tk.LEFT, padx=5)
        records_per_page_combo = ttk.Combobox(
            pagination_frame,
            textvariable=self.records_per_page_var,
            values=[5, 10, 20, 50],
            width=5,
            state="readonly"
        )
        records_per_page_combo.pack(side=tk.LEFT, padx=5)
        records_per_page_combo.bind("<<ComboboxSelected>>", self._on_records_per_page_change)

        self.lbl_total = ttk.Label(pagination_frame, textvariable=self.total_records_var)
        self.lbl_total.pack(side=tk.RIGHT, padx=10)

    def _create_statusbar(self):
        self.status_var = tk.StringVar(value="Готов к работе")
        statusbar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        statusbar.pack(side=tk.BOTTOM, fill=tk.X)

    def _refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        records = self.controller.get_current_page_records()
        start_index = (self.controller.get_current_page() - 1) * self.controller.get_records_per_page()

        for i, record in enumerate(records):
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

            self.tree.insert("", tk.END, values=(
                start_index + i + 1,
                student_fio,
                father_fio,
                father_income,
                mother_fio,
                mother_income,
                record.brothers_count,
                record.sisters_count
            ))

        self._update_pagination_info()

    def _update_pagination_info(self):
        current_page = self.controller.get_current_page()
        total_pages = self.controller.get_total_pages()
        total_records = self.controller.get_total_display_count()

        self.page_info_var.set(f"Страница: {current_page} из {total_pages}")
        self.total_records_var.set(f"Всего записей: {total_records}")

        self.btn_first.config(state=tk.NORMAL if current_page > 1 else tk.DISABLED)
        self.btn_prev.config(state=tk.NORMAL if current_page > 1 else tk.DISABLED)
        self.btn_next.config(state=tk.NORMAL if current_page < total_pages else tk.DISABLED)
        self.btn_last.config(state=tk.NORMAL if current_page < total_pages else tk.DISABLED)

    def _first_page(self):
        self.controller.go_to_first_page()
        self._refresh_table()

    def _prev_page(self):
        self.controller.go_to_previous_page()
        self._refresh_table()

    def _next_page(self):
        self.controller.go_to_next_page()
        self._refresh_table()

    def _last_page(self):
        self.controller.go_to_last_page()
        self._refresh_table()

    def _on_records_per_page_change(self, event=None):
        try:
            count = int(self.records_per_page_var.get())
            self.controller.set_records_per_page(count)
            self._refresh_table()
        except ValueError:
            pass

    def _show_add_dialog(self):
        dialog = AddDialog(self.root, self.controller)
        self.root.wait_window(dialog.dialog)
        self._refresh_table()

    def _show_search_dialog(self):
        dialog = SearchDialog(self.root, self.controller)
        self.root.wait_window(dialog.dialog)
        self._refresh_table()

    def _show_delete_dialog(self):
        dialog = DeleteDialog(self.root, self.controller)
        self.root.wait_window(dialog.dialog)
        self._refresh_table()

    def _show_about_dialog(self):
        AboutDialog(self.root)

    def _load_file(self):
        filepath = filedialog.askopenfilename(
            title="Выберите XML-файл для загрузки",
            filetypes=[("XML файлы", "*.xml"), ("Все файлы", "*.*")]
        )
        if filepath:
            success = self.controller.load_from_file(filepath)
            if success:
                self._refresh_table()
                self.status_var.set(f"Загружено из: {filepath}")
                messagebox.showinfo("Успех", f"Загружено {self.controller.get_total_count()} записей")
            else:
                messagebox.showerror("Ошибка", "Не удалось загрузить файл")

    def _save_file(self):
        if self.controller.get_total_count() == 0:
            messagebox.showwarning("Предупреждение", "Нет данных для сохранения")
            return

        filepath = filedialog.asksaveasfilename(
            title="Сохранить в XML-файл",
            defaultextension=".xml",
            filetypes=[("XML файлы", "*.xml"), ("Все файлы", "*.*")]
        )
        if filepath:
            success = self.controller.save_to_file(filepath)
            if success:
                self.status_var.set(f"Сохранено в: {filepath}")
                messagebox.showinfo("Успех", f"Сохранено {self.controller.get_total_count()} записей")
            else:
                messagebox.showerror("Ошибка", "Не удалось сохранить файл")

    def _on_closing(self):
        if messagebox.askyesno("Выход", "Вы уверены, что хотите выйти?"):
            self.root.destroy()

    def run(self):
        self.root.mainloop()