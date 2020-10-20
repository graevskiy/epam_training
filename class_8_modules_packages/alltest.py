# file: alltest.py
# Если __all__ не задан, импортируются все имена. Это распространяется только на импорты через "*"
__all__ = ['say_something']

def say_something():
    return some_str

some_str = "Hello!"
some_dict = {"a": 1}
some_int = 42
