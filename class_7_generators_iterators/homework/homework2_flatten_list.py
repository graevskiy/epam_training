# Найдите все четные числа из списка VALUES тремя способами:
# функция, которая возвращает List[int]
# функция, которая возвращает Generator
# функция, которая возвращает List[int], но используя однострочный list comprehension

from typing import Generator
from typing import List

VALUES = [
    [[10, 11, 12], [13, 14, 15], [16, 17, 18]],
    [[19, 20, 21], [22, 23, 24], [25, 26, 27]],
    [[28, 29, 30], [31, 32, 33], [34, 35, 36]],
]

def get_even_for_loop(values: List) -> List[int]:
    """Return all even numbers using classical for loop.
    :param values: input list of lists with values
    :return: list with int values
    """
    res = []
    for i in values:
        if isinstance(i, list):
            res.extend(get_even_for_loop(i))
        else:
            if i % 2 == 0:
                res.append(i)
    return res

def get_even_for_loop_iterator(values: List) -> Generator:
    """Return all even numbers using classical for loop.
    :param values: input list of lists with values
    :return: generator with int values
    """
    for i in values:
        if isinstance(i, list):
            yield from get_even_for_loop_iterator(i)
        else:
            if i % 2 == 0:
                yield i

def get_even_list_comprehension(values: List) -> List[int]:
    """Return all even numbers in ONE LINE using list comprehension.
    :param values: input list of lists with values
    :return: list with int values
    """
    return [
        val for row in values for col in row for val in col if val % 2 == 0
    ]

print(get_even_for_loop(VALUES))
print(list(get_even_for_loop_iterator(VALUES)))
print(get_even_list_comprehension(VALUES))

# [10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36]
# [10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36]
# [10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36]
