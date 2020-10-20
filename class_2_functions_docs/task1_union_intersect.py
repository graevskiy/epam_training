# Task 1
# Дописать универсальные функции работы с множествами​.
# Функции должны принимать произвольное число аргументов разных типов: list, tuple, set.
# Возвращать должны set. 
 
# >>> intersect(s1, s2), union(s1, s2) # Два операнда​
# ([‘S’, ‘A’, ‘M’], [‘S’, ‘P’, ‘A’, ‘M’, ‘C’])​
# >>> intersect([1,2,3], (1,4)) # Смешивание типов​
# [1]

def union(*args) -> set:
    a = set()
    for arg in args:
      a = a.union(arg)
    return a
    
def intersect(*args) -> set:
  a = None
  for arg in args:
    a = a or set(arg)
    a = a.intersection(set(arg))
  return a

s1 = 'ABC'
s2 = [1,2,3]
s3 = [3, 6, 7, 'a', 'A']

print(union(s1, s2, s3))
print(intersect(s1, s2, s3))