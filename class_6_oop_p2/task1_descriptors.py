# Создать класс Book с аттрибутами price, author, name.

# Автор и название книги не должны меняться. (Выкидываем ValueError)
# Цена может меняться, но должна находится в пределах: 0 <= price <= 100 

 
# >>> b = Book("William Faulkner", "The Sound and the Fury", 12)

# >>> print(f"Author='{b.author}', Name='{b.name}', Price='{b.price}'")
# Author='William Faulkner', Name='The Sound and the Fury', Price='12'

# >>> b.price = 55
# >>> b.price
# 55
# >>> b.price = -12  # => ValueError: Price must be between 0 and 100.
# >>> b.price = 101  # => ValueError: Price must be between 0 and 100.

# >>> b.author = "new author"  # => ValueError: Author can not be changed.
# >>> b.name = "new name"      # => ValueError: Name can not be changed.

class PriceControl:
    def __set_name__(self, owner, name):
      self.name = name

    def __set__(self, instance, value):
      if not (0 <= value <= 100):
        raise ValueError(f"{type(self).__name__} must be between 0 and 100")
      instance.__dict__[self.name] = value
      
class NameControl:
    def __set_name__(self, owner, name):
      self.name = name

    def __set__(self, instance, value):
      if self.name in instance.__dict__:
        raise ValueError(f"{type(self).__name__} can not be changed")
      instance.__dict__[self.name] = value


class Book:
    author = NameControl()
    name = NameControl()
    price = PriceControl()

    def __init__(self, author, name, price):
      self.author = author
      self.name = name
      self.price = price


b = Book("William Faulkner", "The Sound and the Fury", 12)
print(f"Author='{b.author}', Name='{b.name}', Price='{b.price}'")

b.price = 55
print(b.price)
