# Задание 2. Менеджеры контекста

# Написать контекстный менеджер cd, который меняет текущую директорию на заданную.  

# При входе в контекст нужно запомнить прежнюю директорию и при выходе восстановить ее.  

# При инициализации менеджера проверьте, что переданный путь существует и это директория. 
# Если нет, то выбрасывается ValueError.

# Используйте методы из модуля os: getcwd, chdir, path.isdir

import os


class cd:
    # your code here
    def __init__(self, path):
        if not os.path.isdir(path):
            raise ValueError(f"{path} not a directory")
        self.orig_path = os.getcwd()
        self.path = path

    def __enter__(self):
        os.chdir(self.path)

    def __exit__(self, exc_t, exc_v, exc_tb):        
        os.chdir(self.orig_path)


if __name__ == '__main__':
    with cd('.') as cm:
        print(f'I am in {os.getcwd()}')