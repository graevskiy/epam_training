# Создайте свой аналог zip с точно таким же поведением и который тоже возвращает итератор.
# При реализации нельзя использовать zip, itertools или другие сторонние модули.

# >>> list(zip(['A', 'B', 'C'], [1, 2, 3]))
#     [('A', 1), ('B', 2), ('C', 3)]

# >>> list(zip('!', ['A', 'B', 'C', 'D'], range(1, 3)))
#     [('!', 'A', 1)]

# >>> list(zip('abcd', ['A', 'B', 'C', 'D'], range(0, 40)))
#     [('a', 'A', 0), ('b', 'B', 1), ('c', 'C', 2), ('d', 'D', 3)]

# Используйте что сочтете нужным:
# Или класс
# class CustomZip:
#     pass

# list(CustomZip(['A', 'B', 'C'], [1, 2, 3], (22, 33, 44, 55, 66)))
# # [('A', 1, 22), ('B', 2, 33), ('C', 3, 44)]

# Или функцию:
# def CustomZip():
#     pass

# list(custom_zip(['A', 'B', 'C'], [1, 2, 3], (22, 33, 44, 55, 66)))
# # [('A', 1, 22), ('B', 2, 33), ('C', 3, 44)]

# Используйте имя класса/функции "CustomZip" в каждом случае для простоты тестирования.


from typing import Generator, Iterable

def CustomZip(*args: Iterable) -> Generator:
    """Works like a standard zip function from built-ins
    takes an arbitrary iterable objects and returns generator
    Stops once shortest iterable is exhausted
    try - catch block are needed as per following posts:
    https://stackoverflow.com/questions/16465313/
    how-yield-catches-stopiteration-exception
    https://www.python.org/dev/peps/pep-0479/
    
    :param *args: iterables
    :rtype: generator
    """
    iters = list(map(iter, args))
    while True:
        try:            
            yield tuple(next(i) for i in iters)
        except:
            return


list(CustomZip(['A', 'B', 'C'], [1, 2, 3], (22, 33, 44, 55, 66)))
# >> [('A', 1, 22), ('B', 2, 33), ('C', 3, 44)]

