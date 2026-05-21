"""
Модуль контроллера для приложения "Учёт семей студентов".
Реализует бизнес-логику: управление записями, поиск, удаление, пагинация.
"""

import os
from typing import List, Dict, Any, Optional
from model.student_record import StudentRecord
from model.data_manager import DataManager


class AppController:
    """
    Контроллер приложения. Обрабатывает бизнес-логику и управляет данными.
    """

    def __init__(self):
        """Инициализация контроллера."""
        self.records: List[StudentRecord] = []
        self.filtered_records: List[StudentRecord] = []
        self.current_page: int = 1
        self.records_per_page: int = 10
        self.current_file_path: Optional[str] = None

    # ==================== Управление записями ====================

    def add_record(self, record: StudentRecord) -> bool:
        """
        Добавляет новую запись в массив.

        Args:
            record: Объект StudentRecord для добавления

        Returns:
            True если добавление успешно, иначе False
        """
        # Валидация записи
        is_valid, error_msg = record.validate()
        if not is_valid:
            print(f"Ошибка валидации: {error_msg}")
            return False

        self.records.append(record)
        self._clear_filter()
        return True

    def delete_records(self, criteria: Dict[str, Any]) -> int:
        """
        Удаляет записи, соответствующие критериям.

        Args:
            criteria: Словарь с критериями удаления

        Returns:
            Количество удалённых записей
        """
        if not criteria:
            return 0

        # Находим индексы записей для удаления
        indices_to_delete = []
        for i, record in enumerate(self.records):
            if record.matches_search_criteria(criteria):
                indices_to_delete.append(i)

        # Удаляем записи (с конца, чтобы не сбивать индексы)
        deleted_count = 0
        for i in sorted(indices_to_delete, reverse=True):
            del self.records[i]
            deleted_count += 1

        # Очищаем фильтр и обновляем пагинацию
        self._clear_filter()
        if deleted_count > 0:
            # Корректируем текущую страницу
            total_pages = self.get_total_pages()
            if self.current_page > total_pages and total_pages > 0:
                self.current_page = total_pages
            elif total_pages == 0:
                self.current_page = 1

        return deleted_count

    def update_record(self, index: int, record: StudentRecord) -> bool:
        """
        Обновляет существующую запись.

        Args:
            index: Индекс записи в массиве
            record: Новые данные записи

        Returns:
            True если обновление успешно
        """
        if index < 0 or index >= len(self.records):
            return False

        is_valid, error_msg = record.validate()
        if not is_valid:
            print(f"Ошибка валидации: {error_msg}")
            return False

        self.records[index] = record
        self._clear_filter()
        return True

    def get_all_records(self) -> List[StudentRecord]:
        """
        Возвращает все записи.

        Returns:
            Список всех записей
        """
        return self.records.copy()

    def get_total_count(self) -> int:
        """
        Возвращает общее количество записей.

        Returns:
            Количество записей
        """
        return len(self.records)

    def clear_all_records(self) -> None:
        """Очищает все записи."""
        self.records.clear()
        self._clear_filter()

    # ==================== Поиск ====================

    def search_records(self, criteria: Dict[str, Any]) -> List[StudentRecord]:
        """
        Ищет записи по заданным критериям.

        Args:
            criteria: Словарь с критериями поиска

        Returns:
            Список найденных записей
        """
        if not criteria:
            return []

        found_records = []
        for record in self.records:
            if record.matches_search_criteria(criteria):
                found_records.append(record)

        self.filtered_records = found_records
        return found_records.copy()

    def _clear_filter(self) -> None:
        """Очищает результаты последнего поиска."""
        self.filtered_records = []

    def get_current_display_records(self) -> List[StudentRecord]:
        """
        Возвращает записи для отображения (с учётом фильтра поиска).

        Returns:
            Список записей для отображения
        """
        if self.filtered_records:
            return self.filtered_records
        return self.records

    # ==================== Пагинация ====================

    def get_current_page_records(self) -> List[StudentRecord]:
        """
        Возвращает записи для текущей страницы.

        Returns:
            Список записей на текущей странице
        """
        display_records = self.get_current_display_records()
        total = len(display_records)

        start_index = (self.current_page - 1) * self.records_per_page
        end_index = start_index + self.records_per_page

        if start_index >= total:
            return []
        return display_records[start_index:end_index]

    def get_total_display_count(self) -> int:
        """
        Возвращает общее количество отображаемых записей (с учётом фильтра).

        Returns:
            Количество отображаемых записей
        """
        return len(self.get_current_display_records())

    def get_total_pages(self) -> int:
        """
        Возвращает общее количество страниц.

        Returns:
            Количество страниц
        """
        total = self.get_total_display_count()
        if total == 0:
            return 1
        return (total + self.records_per_page - 1) // self.records_per_page

    def get_current_page(self) -> int:
        """
        Возвращает номер текущей страницы.

        Returns:
            Номер текущей страницы
        """
        return self.current_page

    def set_current_page(self, page: int) -> None:
        """
        Устанавливает номер текущей страницы.

        Args:
            page: Номер страницы (начиная с 1)
        """
        total_pages = self.get_total_pages()
        if page < 1:
            self.current_page = 1
        elif page > total_pages:
            self.current_page = total_pages
        else:
            self.current_page = page

    def go_to_first_page(self) -> None:
        """Переходит на первую страницу."""
        self.current_page = 1

    def go_to_last_page(self) -> None:
        """Переходит на последнюю страницу."""
        self.current_page = self.get_total_pages()

    def go_to_previous_page(self) -> None:
        """Переходит на предыдущую страницу."""
        if self.current_page > 1:
            self.current_page -= 1

    def go_to_next_page(self) -> None:
        """Переходит на следующую страницу."""
        if self.current_page < self.get_total_pages():
            self.current_page += 1

    def set_records_per_page(self, count: int) -> None:
        """
        Устанавливает количество записей на странице.

        Args:
            count: Количество записей (5, 10, 20, 50)
        """
        if count in [5, 10, 20, 50]:
            # Запоминаем текущую первую запись для сохранения позиции
            current_first_index = (self.current_page - 1) * self.records_per_page
            self.records_per_page = count
            # Восстанавливаем страницу, на которой была первая запись
            new_page = (current_first_index // self.records_per_page) + 1
            self.set_current_page(new_page)

    def get_records_per_page(self) -> int:
        """
        Возвращает количество записей на странице.

        Returns:
            Количество записей на странице
        """
        return self.records_per_page

    # ==================== Работа с файлами ====================

    def save_to_file(self, filepath: str) -> bool:
        """
        Сохраняет все записи в XML-файл.

        Args:
            filepath: Путь к файлу

        Returns:
            True если сохранение успешно
        """
        try:
            # Убеждаемся, что директория существует
            directory = os.path.dirname(filepath)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)

            success = DataManager.save_to_file(filepath, self.records)
            if success:
                self.current_file_path = filepath
            return success
        except Exception as e:
            print(f"Ошибка при сохранении: {e}")
            return False

    def load_from_file(self, filepath: str) -> bool:
        """
        Загружает записи из XML-файла.

        Args:
            filepath: Путь к файлу

        Returns:
            True если загрузка успешна
        """
        try:
            records = DataManager.load_from_file(filepath)
            if records is not None:
                self.records = records
                self._clear_filter()
                self.current_page = 1
                self.current_file_path = filepath
                return True
            return False
        except Exception as e:
            print(f"Ошибка при загрузке: {e}")
            return False

    def get_current_file_path(self) -> Optional[str]:
        """
        Возвращает путь к текущему открытому файлу.

        Returns:
            Путь к файлу или None
        """
        return self.current_file_path

    def has_unsaved_changes(self) -> bool:
        """
        Проверяет, есть ли несохранённые изменения.
        (Упрощённая версия)
        """
        return self.current_file_path is None and len(self.records) > 0

    # ==================== Вспомогательные методы ====================

    def get_record_by_index(self, index: int) -> Optional[StudentRecord]:
        """
        Возвращает запись по индексу.

        Args:
            index: Индекс записи

        Returns:
            Запись или None
        """
        if 0 <= index < len(self.records):
            return self.records[index]
        return None

    def get_display_index(self, record_index: int) -> int:
        """
        Возвращает индекс записи в отображаемом списке.

        Args:
            record_index: Индекс в основном массиве

        Returns:
            Индекс в отображаемом списке или -1
        """
        display_records = self.get_current_display_records()
        for i, record in enumerate(display_records):
            if id(record) == id(self.records[record_index]):
                return i
        return -1