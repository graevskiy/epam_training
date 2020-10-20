# Task 1 Timeit
# Написать декоратор, который будет считать время работы функции и выводить на экран. Для текущего времени можно использовать модуль time.​ 



# >> long_running()
# 0.212341254
# complete

import time
from functools import wraps

def print_run_time(func: callable) -> callable:
    #raise NotImplementedError('Implement me!')
    @wraps(func)
    def wrapper(*args, **kwargs):
      start = time.time()
      val = func(*args, **kwargs)
      stop = time.time()
      print(round(stop - start, 9))
      return val
    return wrapper
    

@print_run_time
def long_running():
    time.sleep(0.2)
    return 'complete'
    
long_running()