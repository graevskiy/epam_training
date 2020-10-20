# Необходимо написать фабрику декораторов(также декоратор).
# Фабрика принимает на вход функцию (lambda) возвращает декоратор, который вернет результат выполнения функции в которую первым аргументом передается результат выполнения декорируемой функции. Пример:

# @apply(lambda user_id: user_id + 1)
# def return_user_id():
#   return 42

# >> return_user_id()
# 43

# Не забываем про документацию!

from functools import wraps

def apply(modifier_func: callable) -> callable:
    """ Decorator applying `modifier_func` to a result of decorated function

    :param modifier_func: function which is invoked on a result 
    of decorated function
    :return: decorator function
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwars):
            return modifier_func(func(*args, **kwars))
        return wrapper
    return decorator