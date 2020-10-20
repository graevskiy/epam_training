# Разработайте программу по следующему описанию и следуя принципам ООП.

# В некой игре-стратегии есть солдаты и герои (все они являются воинами).
# У всех есть уникальный номер объекта и принадлежность к команде.
# У солдат есть метод "иду за героем", который в качестве аргумента принимает объект типа "герой".
# У героев есть метод увеличения собственного уровня.

# Всего существует 3 команды, каждая со своим цветом ("red", "yellow", "green").
# У каждой команды есть 1 свой герой.

# В цикле генерируются объекты-солдаты (1 000 шт).
# Их принадлежность к команде определяется случайно.
# Солдаты разных команд добавляются в разные списки.

# Измеряется длина списков солдат противоборствующих команд и выводится на экран.

#     >> Team 'red' has '315' soldiers.
#     >> Team 'yellow' has '376' soldiers.
#     >> Team 'green' has '309' soldiers.
#     >> Team 'yellow' has more soldiers than others.

# У героя, принадлежащего команде с более длинным списком, поднимается уровень на +1.
# Изначально у каждого героя произвольный уровень от 0 до 1.
# У солдат уровня нет.

# Для команды с героем максимального уровня создайте разведывательный отряд из героя и 3х произвольных солдат его команды, которые следуют за ним.
# Выведите на экран состав участников отряда.

#   >> Scout: Soldier(idx=56, color=yellow, hero=Hero(idx=1, color=yellow, level=2))
#   >> Scout: Soldier(idx=505, color=yellow, hero=Hero(idx=1, color=yellow, level=2))
#   >> Scout: Soldier(idx=770, color=yellow, hero=Hero(idx=1, color=yellow, level=2))
#   >> Scout: Hero(idx=1, color=yellow, level=2)

#     (Для красивого вывода можно переписать метод "__repr__".)

# На этом подготовка к битве закончена.


# Для базовой проверки и форматирования кода используйте: isort, black, pylint.
# ДЗ нужно выполнить до следующей лекции.


import random


class Warrior:
    __idx = 0

    def __init__(self, color: str):
        self.idx = self.__class__.__idx
        self.color = color

    @classmethod
    def create(cls, color: str):
        cls.__idx += 1
        return cls(color)

    def __repr__(self):
        descr = ', '.join(
            [f"{k}={v}" for k,v in self.__dict__.items()]
        )
        return f"{self.__class__.__name__}({descr})"


class Hero(Warrior):
    def __init__(self, color: str):
        super().__init__(color=color)
        self.level = random.randint(0, 1)

    def level_increase(self):
        self.level += 1


class Soldier(Warrior):
    def __init__(self, color: str):
        super().__init__(color)
        self.hero = None

    def set_follow_hero(self, hero: Hero):
        self.hero = hero


def main():
    """main logic"""
    colors = ('red', 'yellow', 'green')
    heroes = {}
    for color in colors:
        heroes[color] = Hero.create(color)

    soldiers = {}
    for i in range(1000):
        rand_color = colors[random.randint(0, len(colors) - 1)]
        soldier = Soldier.create(rand_color)
        if rand_color in soldiers:
            soldiers[rand_color].append(soldier)
        else:
            soldiers[rand_color] = [soldier]

    max_count = 0
    for color in colors:
        print(f"Team '{color}' has '{len(soldiers[color])}' soldiers.")
        if max_count < len(soldiers[color]):
            max_count = len(soldiers[color])
            popular_team = color

    heroes[popular_team].level_increase()
    print(f"Team '{popular_team}' has more soldiers than others.")

    scout = random.sample(soldiers[rand_color], 3)

    for character in scout:
        character.set_follow_hero(heroes[popular_team])
        print("Scout:", character)
    print("Scout:", heroes[popular_team])


# run
main()
