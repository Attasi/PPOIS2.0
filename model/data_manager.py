"""
Модуль для управления данными: загрузка и сохранение записей в XML-файл.
Для записи используется DOM парсер, для чтения - SAX парсер.
"""

import os
import xml.dom.minidom
import xml.sax
from xml.sax.handler import ContentHandler
from typing import List
from model.student_record import StudentRecord


class StudentRecordHandler(ContentHandler):
    """
    SAX обработчик для парсинга XML файла с записями о студентах.
    """

    def __init__(self):
        self.records: List[StudentRecord] = []
        self.current_record: dict = {}
        self.current_element: str = ""

    def startElement(self, name: str, attrs) -> None:
        """
        Вызывается при открытии тега.

        Args:
            name: Имя тега
            attrs: Атрибуты тега
        """
        self.current_element = name
        if name == "student":
            self.current_record = {}

    def endElement(self, name: str) -> None:
        """
        Вызывается при закрытии тега.

        Args:
            name: Имя тега
        """
        if name == "student":
            record = StudentRecord.from_dict(self.current_record)
            self.records.append(record)
        self.current_element = ""

    def characters(self, content: str) -> None:
        """
        Вызывается при чтении текстового содержимого тега.

        Args:
            content: Текстовое содержимое
        """
        if not self.current_element:
            return

        content = content.strip()
        if not content:
            return

        self.current_record[self.current_element] = content


class DataManager:
    """
    Класс для сохранения и загрузки записей в XML-файл.
    """

    @staticmethod
    def save_to_file(filename: str, records: List[StudentRecord]) -> bool:
        """
        Сохраняет список записей в XML-файл (использует DOM парсер).

        Args:
            filename: Путь к файлу
            records: Список записей StudentRecord

        Returns:
            True если сохранение успешно, иначе False
        """
        try:
            # Создаём корневой элемент
            doc = xml.dom.minidom.getDOMImplementation().createDocument(
                None, "students", None
            )
            root = doc.documentElement

            # Для каждой записи создаём элемент <student>
            for record in records:
                student_element = doc.createElement("student")

                # Добавляем все поля записи
                fields = record.to_dict()
                for field_name, field_value in fields.items():
                    field_element = doc.createElement(field_name)
                    text_node = doc.createTextNode(str(field_value))
                    field_element.appendChild(text_node)
                    student_element.appendChild(field_element)

                root.appendChild(student_element)

            # Записываем в файл с форматированием
            with open(filename, "w", encoding="utf-8") as f:
                doc.writexml(f, indent="", addindent="    ", newl="\n", encoding="utf-8")

            return True

        except Exception as e:
            print(f"Ошибка при сохранении файла {filename}: {e}")
            return False

    @staticmethod
    def load_from_file(filename: str) -> List[StudentRecord]:
        """
        Загружает список записей из XML-файла (использует SAX парсер).

        Args:
            filename: Путь к файлу

        Returns:
            Список записей StudentRecord, либо пустой список при ошибке
        """
        if not os.path.exists(filename):
            print(f"Файл {filename} не найден")
            return []

        try:
            # Создаём обработчик
            handler = StudentRecordHandler()

            # Создаём парсер и передаём ему обработчик
            parser = xml.sax.make_parser()
            parser.setContentHandler(handler)

            # Парсим файл
            parser.parse(filename)

            return handler.records

        except Exception as e:
            print(f"Ошибка при загрузке файла {filename}: {e}")
            return []

