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

    @staticmethod
    def generate_sample_data(count: int = 50) -> List[StudentRecord]:
        """
        Генерирует тестовые данные для демонстрации работы.

        Args:
            count: Количество генерируемых записей

        Returns:
            Список записей StudentRecord
        """
        records = []

        # Списки для генерации осмысленных данных
        lastnames = ["Иванов", "Петров", "Сидоров", "Кузнецов", "Смирнов", "Васильев",
                     "Федоров", "Михайлов", "Новиков", "Морозов", "Волков", "Алексеев"]
        firstnames_male = ["Александр", "Дмитрий", "Максим", "Сергей", "Андрей", "Алексей",
                           "Владимир", "Николай", "Евгений", "Михаил", "Павел", "Игорь"]
        firstnames_female = ["Елена", "Ольга", "Наталья", "Ирина", "Светлана", "Татьяна",
                             "Анна", "Мария", "Екатерина", "Юлия", "Анастасия", "Дарья"]
        patronymics_male = ["Александрович", "Дмитриевич", "Максимович", "Сергеевич",
                            "Андреевич", "Алексеевич", "Владимирович", "Николаевич"]
        patronymics_female = ["Александровна", "Дмитриевна", "Максимовна", "Сергеевна",
                              "Андреевна", "Алексеевна", "Владимировна", "Николаевна"]

        for i in range(count):
            # Выбираем случайный пол студента для разнообразия
            student_gender = i % 2
            parent_gender = (i // 2) % 2

            # ФИО студента
            if student_gender == 0:
                student_fn = firstnames_male[i % len(firstnames_male)]
                student_pat = patronymics_male[i % len(patronymics_male)]
            else:
                student_fn = firstnames_female[i % len(firstnames_female)]
                student_pat = patronymics_female[i % len(patronymics_female)]

            student_ln = lastnames[i % len(lastnames)]

            # ФИО отца
            father_fn = firstnames_male[(i + 1) % len(firstnames_male)]
            father_pat = patronymics_male[(i + 2) % len(patronymics_male)]
            father_ln = student_ln

            # ФИО матери
            mother_fn = firstnames_female[(i + 3) % len(firstnames_female)]
            mother_pat = patronymics_female[(i + 4) % len(patronymics_female)]
            mother_ln = student_ln + "а"

            # Доходы (от 20000 до 150000)
            father_income = 20000 + (i * 1234) % 130000
            mother_income = 20000 + (i * 2345) % 130000

            # Количество братьев и сестер (0-3)
            brothers = (i * 7) % 4
            sisters = (i * 11) % 4

            record = StudentRecord(
                student_lastname=student_ln,
                student_firstname=student_fn,
                student_patronymic=student_pat,
                father_lastname=father_ln,
                father_firstname=father_fn,
                father_patronymic=father_pat,
                father_income=float(father_income),
                mother_lastname=mother_ln,
                mother_firstname=mother_fn,
                mother_patronymic=mother_pat,
                mother_income=float(mother_income),
                brothers_count=brothers,
                sisters_count=sisters
            )
            records.append(record)

        return records

    @staticmethod
    def save_sample_to_file(filename: str, count: int = 50) -> bool:
        """
        Генерирует и сохраняет тестовые данные в файл.

        Args:
            filename: Путь к файлу
            count: Количество записей

        Returns:
            True если сохранение успешно
        """
        records = DataManager.generate_sample_data(count)
        return DataManager.save_to_file(filename, records)


def create_test_data_file() -> None:
    """
    Создаёт тестовый файл data.xml с 50 записями в папке resources/data/
    """
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources", "data")
    os.makedirs(data_dir, exist_ok=True)

    filepath = os.path.join(data_dir, "students.xml")
    DataManager.save_sample_to_file(filepath, 50)
    print(f"Тестовый файл создан: {filepath}")
    print(f"Создано 50 записей")