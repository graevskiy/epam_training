# Реализовать абстрактный класс валюты, с наследниками Euro, Dollar, Rubble.
# Курс пусть будет 1 EUR == 2 USD == 100 RUB

# Имплементировать методы из примеров ниже:

 
# print(
#     f"Euro.course(Rubble)   ==> {Euro.course(Rubble)}\n"
#     f"Dollar.course(Rubble) ==> {Dollar.course(Rubble)}\n"
#     f"Rubble.course(Euro)   ==> {Rubble.course(Euro)}\n"
# )
# # Euro.course(Rubble)   ==> 100.0 RUB for 1 EUR
# # Dollar.course(Rubble) ==> 50.0 RUB for 1 USD
# # Rubble.course(Euro)   ==> 0.01 EUR for 1 RUB

# e = Euro(100)
# r = Rubble(100)
# d = Dollar(200)

# print(
#     f"e = {e}\n"
#     f"e.to(Dollar) = {e.to(Dollar)}\n"
#     f"e.to(Rubble) = {e.to(Rubble)}\n"
#     f"e.to(Euro)   = {e.to(Euro)}\n"
# )
# # e = 100 EUR
# # e.to(Dollar) = 200.0 USD
# # e.to(Rubble) = 10000.0 RUB
# # e.to(Euro)   = 100.0 EUR

# print(
#     f"r = {r}\n"
#     f"r.to(Dollar) = {r.to(Dollar)}\n"
#     f"r.to(Euro)   = {r.to(Euro)}\n"
#     f"r.to(Rubble) = {r.to(Rubble)}\n"
# )
# # r = 100 RUB
# # r.to(Dollar) = 2.0 USD
# # r.to(Euro)   = 1.0 EUR
# # r.to(Rubble) = 100.0 RUB

# print(
#     f"e > r   ==> {e > r}\n"
#     f"e == d  ==> {e == d}\n"
# )
# # e > r   ==> True
# # e == d  ==> True

# print(
#     f"e + r  =>  {e + r}\n"
#     f"r + d  =>  {r + d}\n"
#     f"d + e  =>  {d + e}\n"
# )
# # e + r  =>  101.0 EUR
# # r + d  =>  10100.0 RUB
# # d + e  =>  400.0 USD

# print(sum([Euro(i) for i in range(5)]))
# # 10.0 EUR


from abc import ABC, abstractmethod
from functools import total_ordering


@total_ordering
class Currency(ABC):
    """
    Defines abstract class of currency
    1 EUR = 2 USD = 100 RUB
    """

    __slots__ = ("amount", "arc")

    def __init__(self, amount: float):
        self.amount = amount

    @property
    @abstractmethod
    def acr(self):
        """Acronym of a currency. Usually three uppercased letters"""
        pass

    # can't make it to be a class method
    # but this should be a class level property
    # defined in each subclass
    @property
    @abstractmethod
    def base_rate(cls):
        """Something called abstract base rate.
        Used as a base rate for all conversions.
        """
        pass

    @classmethod
    def exchange_rate(cls, other) -> float:
        """Get exchange ratio between subclasses of `Currency`

        :param other: a class that ratio will be calculated
        :type other: subclass of `Currency`
        :return: ratio of base rates
        :rtype: float
        """
        return other.base_rate / cls.base_rate

    @classmethod
    def course(cls, other) -> str:
        """Public method - string representation of `exchange_rate`

        :param other: a class that ratio will be calculated
        :type other: subclass of `Currency`
        :return: prettified string representing exchange ratio
        :rtype: string
        """
        return f"{cls.exchange_rate(other)} {other.acr} for 1 {cls.acr}"

    def to(self, other):
        """Creates instance of `other` currency from a given `self`
        re-calculates amount from `self` currency to `other`

        :param other: a class which instance we'll create and return
        :type other: subclass of `Currency`
        :return: object of `other` from `self`
        :rtype: instance of `other's` class
        """
        return other(self.amount * type(self).exchange_rate(other))

    def convert(self, other):
        """Does inversion of `to` method. Converts instance `other`
        to instance of `self`. More of less is used internally for
        comparison and addition magic methods.

        :param other: another instance of currency we want to convert
        :type other: instance of subclass of `Currency`
        :return: converted currency item
        :rtype: instance of class of `self`
        """
        return other.to(type(self))

    def __eq__(self, other):
        return self.amount == self.convert(other).amount

    def __lt__(self, other):
        return self.amount < self.convert(other).amount

    def __add__(self, other):
        """Re-load magic method to be able to add items
        Check if `other` is an instance of a subclass.
        If yes, add their `amounts` and return new instance.
        If not, assume `other` is addable (like int or float)
        and do straight addition

        :param other: something we add to `self`
        :type other: instance of a subclass of `Currency` or other addable item
        :return: new item with updated (added) amount
        :rtype: instance of class of `self`
        """
        if isinstance(other, Currency):
            overall_amount = self.convert(other).amount
        else:
            overall_amount = other
        overall_amount += self.amount
        return type(self)(overall_amount)

    def __radd__(self, other):
        return self.__add__(other)

    def __repr__(self):
        return f"{self.amount} {self.acr}"


class Euro(Currency):
    base_rate = 1
    acr = "EUR"


class Dollar(Currency):
    base_rate = 2
    acr = "USD"


class Rubble(Currency):
    base_rate = 100
    acr = "RUB"


print(
    f"Euro.course(Rubble)   ==> {Euro.course(Rubble)}\n"
    f"Dollar.course(Rubble) ==> {Dollar.course(Rubble)}\n"
    f"Rubble.course(Euro)   ==> {Rubble.course(Euro)}\n"
)

e = Euro(100)
r = Rubble(100)
d = Dollar(200)

print(
    f"e = {e}\n"
    f"e.to(Dollar) ==> {e.to(Dollar)}\n"
    f"e.to(Rubble) ==> {e.to(Rubble)}\n"
    f"e.to(Euro)   ==> {e.to(Euro)}\n"
)
print(
    f"r = {r}\n"
    f"r.to(Dollar) ==> {r.to(Dollar)}\n"
    f"r.to(Euro)   ==> {r.to(Euro)}\n"
    f"r.to(Rubble) ==> {r.to(Rubble)}\n"
)

print(f"e > r  ==> {e > r}\n" f"e == d ==> {e == d}\n")

print(f"e + r  =>  {e + r}\n" f"r + d  =>  {r + d}\n" f"d + e  =>  {d + e}\n")

print(sum([Euro(i) for i in range(5)]))
