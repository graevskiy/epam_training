# Task 3 Inheritance
# Создать класс "SchoolMember" который представляет любого человека в школе. 
# Класс "Teacher" наследуется от "SchoolMember" .
# Класс "Student" наследуется от "SchoolMember".
 
# Классы должны иметь одинаковый интерфейс с публичной функцией "show()".

# Пример:

# >>> persons = [Teacher("Mr.Poopybutthole", 40, 3000), Student("Morty", 16, 75)]

# (Created Teacher: Mr.Poopybutthole)
# (Created Student: Morty)

# >>> for person in persons:
#             person.show()

# Name: Mr.Poopybutthole, Age: 40, Salary: 3000
# Name: Morty, Age: 16, Grades: 75

# NOTES FROM TEACHER:
# Можно и так, но лучше использовать меньше магии вроде "self.__dict__.items()"
# Т.к. с первого взгляда не ясно что мы увидим вызвав show()

from typing import Any

class SchoolMember:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
        self.__protected_prop = 222

    def __get_dict(self):
        return {
            k: v
            for k, v in self.__dict__.items() if not k[0].startswith('_')
        }

    def _pretty_print(self, key: Any, val: Any):
        return key.title() + ': ' + str(val)

    def show(self):
        return ', '.join(
            self._pretty_print(k, v)
            for (k, v) in self.__get_dict().items()
        )


class Teacher(SchoolMember):
    def __init__(self, name: str, age: int, salary: int):
        super().__init__(name, age)
        self.salary = salary

class Student(SchoolMember):
    def __init__(self, name: str, age: int, grades: int):
        super().__init__(name, age)
        self.grades = grades
        
persons = [Teacher("Mr.Poopybutthole", 40, 3000), Student("Morty", 16, 75)]

for person in persons:
    print(person.show())