#  У вас есть данные формата ​
# [{name: ‘Alexey’, rate: 2, course: ‘Python’}, …]​
# ​
# Выведите топ студентов по каждому из предметов​,

# например: {'Python': 'Alexey'}

from typing import List
from operator import itemgetter as g

def get_top(data: List[dict]) -> dict:
    """ Creates dict with `course` values as keys
    and `names` as values taking only highest ranks
    
    :param data: list of dicts representing a 'student' entity
    :returns: dict 'course_name': 'student_name' of students with highest scores
    """
    return {
      d['course']: d['name'] 
      for d in sorted(data, key=g('rate'))
    }