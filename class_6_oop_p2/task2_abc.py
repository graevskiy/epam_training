# Создать абстрактный класс Vehicle с методами:
# vehicle_type, который выводит имя и тип транспортного средства (ТС),
# is_motorcycle, который выводит True/False в зависимости от числа колес (2 колеса -> мотоцикл),
# purchase_price - выводит стоимость ТС в зависимости от кол-ва пройденных км: (базовая цена - 0.1 * кол-во км).
# Если получился меньше "100" - вернуть "100".

# Класс должен содержать поля:
# год выпуска
# имя бренда
# все поля необходимые для обеспечения функциональности классов наследников.

# Расставить где необходимо и если необходимо abstractmethod, classmethod, staticmethod или другие декораторы.
# Создать классы наследники Vehicle: Car, Motorcycle, Truck, Bus.
 
# vehicles = (
#     Car(brand_name="Toyota", year_of_issue=2020, base_price=1_000_000, mileage=150_000),
#     Motorcycle(brand_name="Suzuki", year_of_issue=2015, base_price=800_000, mileage=35_000),
#     Truck(brand_name="Scania", year_of_issue=2018, base_price=15_000_000, mileage=850_000),
#     Bus(brand_name="MAN", year_of_issue=2000, base_price=10_000_000, mileage=950_000),
# )

# for vehicle in vehicles:
#     print(
#         f"Vehicle type={vehicle.vehicle_type()}\n"
#         f"Is motorcycle={vehicle.is_motorcycle()}\n"
#         f"Purchase price={vehicle.purchase_price()}\n"
#     )

# Vehicle type=Toyota Car
# Is motorcycle=False
# Purchase price=985000.0

# Vehicle type=Suzuki Motorcycle
# Is motorcycle=True
# Purchase price=796500.0

# Vehicle type=Scania Truck
# Is motorcycle=False
# Purchase price=14915000.0

# Vehicle type=MAN Bus
# Is motorcycle=False
# Purchase price=9905000.0


from abc import ABC, abstractmethod


class Vehicle(ABC):
    """ Implements abstract interface for a standard `Vehicle` with 4 wheels"""

    num_of_wheels = 4

    def __init__(
        self, brand_name: str, year_of_issue: int, base_price: int, mileage: int
    ):
        """ Initializes  necessary attributes for an abstract vehicle"""

        self.brand_name = brand_name
        self.year_of_issue = year_of_issue
        self.base_price = base_price
        self.mileage = mileage

    def vehicle_type(self) -> str:
        """ Representation of a vehicle with brand name and given class name"""
        return f"{self.brand_name} {type(self).__name__}"

    @classmethod
    def is_motorcycle(cls) -> bool:
        """ Defines if a vehicle is a motorcycle. Class method"""
        return cls.num_of_wheels == 2

    def purchase_price(self) -> float:
        return max(100, self.base_price - self.mileage * 0.1)


class Car(Vehicle):
    pass


class Motorcycle(Vehicle):
    num_of_wheels = 2


class Truck(Vehicle):
    pass


class Bus(Vehicle):
    pass


vehicles = (
    Car(brand_name="Toyota", year_of_issue=2020, base_price=1_000_000, mileage=150_000),
    Motorcycle(
        brand_name="Suzuki", year_of_issue=2015, base_price=800_000, mileage=35_000
    ),
    Truck(
        brand_name="Scania", year_of_issue=2018, base_price=15_000_000, mileage=850_000
    ),
    Bus(brand_name="MAN", year_of_issue=2000, base_price=10_000_000, mileage=950_000),
)

for vehicle in vehicles:
    print(
        f"Vehicle type={vehicle.vehicle_type()}\n"
        f"Is motorcycle={vehicle.is_motorcycle()}\n"
        f"Purchase price={vehicle.purchase_price()}\n"
    )
