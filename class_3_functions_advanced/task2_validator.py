# Task 2 Validator
# Написать декоратор validate, который будет валидировать входящие аргументы функции на предмет выхода за заданные границы
# Если параметры верны, должен возвращать вывод функции. Если нет, должен возвращать строку "Function call is not valid!​"

# >>> @validate(low_bound=0, upper_bound=256)​
# ... def set_pixel(red, green, blue):​
# ...     print("Pixel created!")​
# ... ​
# >>> set_pixel(0, 127, 300)​
# Function call is not valid!​
# >>> set_pixel(0, 127, 250) ​
# Pixel created!​
# ​
# Не забываем про документацию!

from typing import Any, Optional
from functools import wraps

def validate(low_bound: int=0, upper_bound: int=256) -> callable:
    """ Decorator function with two arguments - low/high limits.
    calls inner function if constraints match, 
    returns warning string otherwise
    
    :param lower_bound int: lower bound for args for inner func
    :param upper_bound int: upper bound for args for inner func
    
    :returns: result of func `set_pixel` call or warning string
    :rtype: str
    """
    def validate_decor(func: callable) -> callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Optional:
            if min(args) < low_bound or max(args) > upper_bound:
                return 'Function call is not valid!'
            return func(*args, **kwargs)
        return wrapper
    return validate_decor
        
                
@validate()
def set_pixel(red: int, green: int, blue: int) -> str:
    """Just create a pixel"""
    return "Pixel created!"
    