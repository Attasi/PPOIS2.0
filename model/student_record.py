"""
Модуль с моделью данных для учёта семей студентов.
Содержит класс StudentRecord - одну запись о студенте и его семье.
"""

from typing import Dict, Any, Optional


class StudentRecord:
    """
    Класс, представляющий одну запись о студенте и его семье.

    Атрибуты:
    - student_lastname, student_firstname, student_patronymic: ФИО студента
    - father_lastname, father_firstname, father_patronymic: ФИО отца
    - father_income: заработок отца
    - mother_lastname, mother_firstname, mother_patronymic: ФИО матери
    - mother_income: заработок матери
    - brothers_count: количество братьев
    - sisters_count: количество сестер
    """

    def __init__(
            self,
            student_lastname: str = "",
            student_firstname: str = "",
            student_patronymic: str = "",
            father_lastname: str = "",
            father_firstname: str = "",
            father_patronymic: str = "",
            father_income: float = 0.0,
            mother_lastname: str = "",
            mother_firstname: str = "",
            mother_patronymic: str = "",
            mother_income: float = 0.0,
            brothers_count: int = 0,
            sisters_count: int = 0
    ):
        """
        Конструктор класса StudentRecord.

        Args:
            student_lastname: Фамилия студента
            student_firstname: Имя студента
            student_patronymic: Отчество студента
            father_lastname: Фамилия отца
            father_firstname: Имя отца
            father_patronymic: Отчество отца
            father_income: Заработок отца
            mother_lastname: Фамилия матери
            mother_firstname: Имя матери
            mother_patronymic: Отчество матери
            mother_income: Заработок матери
            brothers_count: Количество братьев
            sisters_count: Количество сестер
        """
        self.student_lastname = student_lastname.strip()
        self.student_firstname = student_firstname.strip()
        self.student_patronymic = student_patronymic.strip()

        self.father_lastname = father_lastname.strip()
        self.father_firstname = father_firstname.strip()
        self.father_patronymic = father_patronymic.strip()
        self.father_income = float(father_income) if father_income else 0.0

        self.mother_lastname = mother_lastname.strip()
        self.mother_firstname = mother_firstname.strip()
        self.mother_patronymic = mother_patronymic.strip()
        self.mother_income = float(mother_income) if mother_income else 0.0

        self.brothers_count = int(brothers_count) if brothers_count else 0
        self.sisters_count = int(sisters_count) if sisters_count else 0

    def to_dict(self) -> Dict[str, Any]:
        """
        Преобразует объект в словарь.

        Returns:
            Словарь со всеми атрибутами объекта
        """
        return {
            "student_lastname": self.student_lastname,
            "student_firstname": self.student_firstname,
            "student_patronymic": self.student_patronymic,
            "father_lastname": self.father_lastname,
            "father_firstname": self.father_firstname,
            "father_patronymic": self.father_patronymic,
            "father_income": self.father_income,
            "mother_lastname": self.mother_lastname,
            "mother_firstname": self.mother_firstname,
            "mother_patronymic": self.mother_patronymic,
            "mother_income": self.mother_income,
            "brothers_count": self.brothers_count,
            "sisters_count": self.sisters_count
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'StudentRecord':
        """
        Создаёт объект StudentRecord из словаря.

        Args:
            data: Словарь с данными

        Returns:
            Объект StudentRecord
        """
        return cls(
            student_lastname=data.get("student_lastname", ""),
            student_firstname=data.get("student_firstname", ""),
            student_patronymic=data.get("student_patronymic", ""),
            father_lastname=data.get("father_lastname", ""),
            father_firstname=data.get("father_firstname", ""),
            father_patronymic=data.get("father_patronymic", ""),
            father_income=data.get("father_income", 0.0),
            mother_lastname=data.get("mother_lastname", ""),
            mother_firstname=data.get("mother_firstname", ""),
            mother_patronymic=data.get("mother_patronymic", ""),
            mother_income=data.get("mother_income", 0.0),
            brothers_count=data.get("brothers_count", 0),
            sisters_count=data.get("sisters_count", 0)
        )

    def validate(self) -> tuple[bool, Optional[str]]:
        """
        Проверяет корректность данных записи.

        Returns:
            Кортеж (успешно_ли_проверка, сообщение_об_ошибке)
        """
        # Проверка ФИО студента
        if not self.student_lastname and not self.student_firstname and not self.student_patronymic:
            return False, "Заполните хотя бы один элемент ФИО студента"

        # Проверка доходов (не могут быть отрицательными)
        if self.father_income < 0:
            return False, "Заработок отца не может быть отрицательным"

        if self.mother_income < 0:
            return False, "Заработок матери не может быть отрицательным"

        # Проверка количества братьев и сестер
        if self.brothers_count < 0:
            return False, "Количество братьев не может быть отрицательным"

        if self.sisters_count < 0:
            return False, "Количество сестер не может быть отрицательным"

        return True, None

    def matches_fio_criteria(self, search_value: str, case_sensitive: bool = False) -> bool:
        """
        Проверяет, совпадает ли любой элемент ФИО студента с поисковым значением.

        Args:
            search_value: Искомое значение
            case_sensitive: Учитывать ли регистр

        Returns:
            True если хотя бы один элемент ФИО совпадает
        """
        if not search_value:
            return True

        if not case_sensitive:
            search_value = search_value.lower()
            student_lastname = self.student_lastname.lower()
            student_firstname = self.student_firstname.lower()
            student_patronymic = self.student_patronymic.lower()
        else:
            student_lastname = self.student_lastname
            student_firstname = self.student_firstname
            student_patronymic = self.student_patronymic

        # Проверяем, содержится ли поисковое значение в любом элементе ФИО
        # (не только полное совпадение, но и частичное)
        return (search_value in student_lastname or
                search_value in student_firstname or
                search_value in student_patronymic)

    def matches_parent_fio_criteria(
            self,
            parent_type: str,
            search_value: str,
            case_sensitive: bool = False
    ) -> bool:
        """
        Проверяет, совпадает ли любой элемент ФИО родителя с поисковым значением.

        Args:
            parent_type: "father" или "mother"
            search_value: Искомое значение
            case_sensitive: Учитывать ли регистр

        Returns:
            True если хотя бы один элемент ФИО родителя совпадает
        """
        if not search_value:
            return True

        if not case_sensitive:
            search_value = search_value.lower()

        if parent_type == "father":
            lastname = self.father_lastname.lower() if not case_sensitive else self.father_lastname
            firstname = self.father_firstname.lower() if not case_sensitive else self.father_firstname
            patronymic = self.father_patronymic.lower() if not case_sensitive else self.father_patronymic
        elif parent_type == "mother":
            lastname = self.mother_lastname.lower() if not case_sensitive else self.mother_lastname
            firstname = self.mother_firstname.lower() if not case_sensitive else self.mother_firstname
            patronymic = self.mother_patronymic.lower() if not case_sensitive else self.mother_patronymic
        else:
            return False

        return (search_value in lastname or
                search_value in firstname or
                search_value in patronymic)

    def matches_siblings_criteria(self, sibling_type: str, count: int) -> bool:
        """
        Проверяет количество братьев или сестер.

        Args:
            sibling_type: "brothers" или "sisters"
            count: Искомое количество

        Returns:
            True если количество совпадает
        """
        if count < 0:
            return True

        if sibling_type == "brothers":
            return self.brothers_count == count
        elif sibling_type == "sisters":
            return self.sisters_count == count
        return False

    def matches_income_criteria(
            self,
            parent_type: str,
            min_income: Optional[float] = None,
            max_income: Optional[float] = None
    ) -> bool:
        """
        Проверяет, попадает ли доход родителя в заданный диапазон.

        Args:
            parent_type: "father" или "mother"
            min_income: Нижняя граница (включительно)
            max_income: Верхняя граница (включительно)

        Returns:
            True если доход входит в диапазон
        """
        if parent_type == "father":
            income = self.father_income
        elif parent_type == "mother":
            income = self.mother_income
        else:
            return False

        if min_income is not None and max_income is not None:
            return min_income <= income <= max_income
        elif min_income is not None:
            return income >= min_income
        elif max_income is not None:
            return income <= max_income
        else:
            return True

    def matches_search_criteria(self, criteria: Dict[str, Any]) -> bool:
        """
        Проверяет, соответствует ли запись критериям поиска.

        Args:
            criteria: Словарь с критериями поиска.
                Возможные ключи:
                - student_fio: {"value": str, "case_sensitive": bool}
                - parent_fio: {"type": str, "value": str, "case_sensitive": bool}
                - siblings: {"type": str, "count": int}
                - income: {"type": str, "min": float, "max": float}

        Returns:
            True если запись соответствует всем указанным критериям
        """
        # Проверка критерия по ФИО студента
        if "student_fio" in criteria:
            student_fio = criteria["student_fio"]
            if not self.matches_fio_criteria(
                    student_fio.get("value", ""),
                    student_fio.get("case_sensitive", False)
            ):
                return False

        # Проверка критерия по ФИО родителя
        if "parent_fio" in criteria:
            parent_fio = criteria["parent_fio"]
            if not self.matches_parent_fio_criteria(
                    parent_fio.get("type", ""),
                    parent_fio.get("value", ""),
                    parent_fio.get("case_sensitive", False)
            ):
                return False

        # Проверка критерия по числу братьев/сестер
        if "siblings" in criteria:
            siblings = criteria["siblings"]
            if not self.matches_siblings_criteria(
                    siblings.get("type", ""),
                    siblings.get("count", -1)
            ):
                return False

        # Проверка критерия по доходу
        if "income" in criteria:
            income = criteria["income"]
            if not self.matches_income_criteria(
                    income.get("type", ""),
                    income.get("min"),
                    income.get("max")
            ):
                return False

        return True

    def __str__(self) -> str:
        """
        Строковое представление записи.

        Returns:
            Строка с ФИО студента
        """
        fio_parts = [self.student_lastname, self.student_firstname, self.student_patronymic]
        fio = " ".join([p for p in fio_parts if p])
        return f"StudentRecord: {fio}"