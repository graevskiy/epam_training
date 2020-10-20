# Task 1 hash
# Преобразовать код в императивном стиле 

# names = ['Alexey', 'Ivan', 'Petr']​
# ​
# for i in range(len(names)):​
#     names[i] = hash(names[i])​
# ​
# print(names)​

# в функциональный.
# функция hash_names на вход принимает список строк, на выход - список интов.

# Не забываем про документацию!

from typing import List

def hash_names(names: List[str]) -> List[int]:
    """ Hashes each element of iterable via standard `hash` function
    
    :param names: list of stings to generate hash of
    :returns: list of hashes (type ints)
    """
    return list(map(hash, names))