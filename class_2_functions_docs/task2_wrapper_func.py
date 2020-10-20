# Task 2
# Написать функцию, которая обертывает любую, 
# передаваемую в нее функцию и возвращает Tuple[имя функции, результат вызова]
def deanon(func: callable) -> callable:
    #raise NotImplemented('Implement me!')
    def inner(*args, **kwargs):
      return func.__name__, func(*args, **kwargs)
    
    return inner
    
    
d = deanon(int)

res = d('123')
print(res)