# Задание 1

# Реализовать контекстный менеджер - аналог tempdir.
# При входе в контекст создается директория с уникальным именем.
# Вся дальнейшая работа ведется в этой директории (она становится текущей).
# При выходе из контекста директория удаляется вместе со всеми файлами в ней.
# Рабочей директорией становиться та, что была до входа в контекст.
# Использовать протокол менеджеров контекста (реализовать методы __enter__ и __exit__).
# Продемонстрировать работу своего менеджера: пока находимся в его контексте, пишем что-нибудь на диск, после выхода - проверяем, что все подчистилось без каких-то дополнительных команд.

import os
import shutil
import time

from pathlib import Path

class temp_dir:
    """ Context manager which creates temp directory
    and moves into it while being inside a context.
    Does a clean up on exit.
    
    """
    def __init__(self):
        dir_name = f"./{int(time.time() * 1000)}"
        Path(dir_name).mkdir()
        self.path = dir_name
        self.orig_path = os.getcwd()

    def __enter__(self):
        os.chdir(self.path)

    def __exit__(self, exc_t, exc_v, exc_tb):
        os.chdir(self.orig_path)
        shutil.rmtree(self.path)        


if __name__ == '__main__':

    curr_dir_items = list(Path('.').iterdir())

    with temp_dir():
        print(f"I'm in {os.getcwd()}")
        with open('example.txt', 'w') as f:
            f.write('hello there')
    print(f"I'm back in {os.getcwd()}")

    assert curr_dir_items == list(Path('.').iterdir())