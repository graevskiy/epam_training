# Task 2 Polymorphism
# В качестве практической работы попробуйте самостоятельно перегрузить оператор сложения.

# Для его перегрузки используется метод "__add__()".
# Он вызывается, когда объекты класса, имеющего данный метод, фигурируют в операции сложения, причем с левой стороны.

# Это значит, что в выражении "a + b" у объекта "a" должен быть метод "__add__()". 
# Объект "b" может быть чем угодно, но чаще всего он бывает объектом того же класса.
# (В нашем случае это будет строка "mississippi")

# Объект "b" будет автоматически передаваться в метод "__add__()" в качестве второго аргумента (первый – "self").

# In:  Counter([1, 2, 3]) + "mississippi"
# Out: ["1 mississippi", "2 mississippi" , "3 mississippi"]

from typing import List, Any


class Counter:
    def __init__(self, values: List[int]):
        self.values = values

    def __add__(self, other: Any):
        if self.__class__ != other.__class__:            
            return [
                    other.__class__(i) + " " + other
                    for i in self.values
            ]
        else:
            return [i + j for i in self.values]

print(Counter([1, 2, 3]) + "mississippi")