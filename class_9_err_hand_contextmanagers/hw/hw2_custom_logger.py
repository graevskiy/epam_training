# Задание 2

# Реализовать контекстный менеджер, выводящий в файл следующую информацию:
# дата
# время выполнения кода
# информация о возникшей ошибке (в коде, обернутом контекстным менеджером).
# Файл указать при конструировании менеджера.
# Файл открывается в режиме append, чтобы при вызове менеджера с одним и тем же файлом информация дописывалась (такой самописный лог).
# Выше ошибка прокидывается (происходит reraise).
# Используйте ContextDecorator для решения.

# NOTE FROM TEACHER:
# Файл лога следует открывать только в __exit__ -  он нужен только там.
# Ну и конечно же делать это с менеджером контекста

import contextlib
import datetime
import time
import traceback


class custom_logging(contextlib.ContextDecorator):
    """Custom logger class. Logs data, time of execution
    and exception raised if any.

    """

    def __init__(self, file: str):
        self.file_name = file
        

    def __enter__(self):
        self.file_obj = open(self.file_name, 'a+', encoding='utf-8')
        self.start_time = time.time()
        print(f"Date: {datetime.date.today()}", file=self.file_obj)

        # return fd as we might want to log something into it
        # while inside context
        return self.file_obj

    def __exit__(self, exc_t, exc_v, exc_tb):
        time_spent = time.time() - self.start_time
        print(f"Time of executing: {time_spent}", file=self.file_obj)
        if exc_v:
            print(traceback.format_exc(), file=self.file_obj)
        else:
            print(file=self.file_obj) #do a line break
        print('closing')
        self.file_obj.close()            

        return False


# this example works just fine
@custom_logging('fib_log.txt')
def bad_fib(n):
    res = [0, 1]
    for i in range(2, n+1):
        res.append(res[i-1] + res[i-2])
    return res[-1]


# this one tries to write to closed file
@custom_logging('fib_log_2.txt')
def bad_fib2(n):
    if n < 2:
        return n
    return bad_fib2(n-1) + bad_fib2(f-2)


if __name__ == '__main__':

    #works fine
    with custom_logging('my_log.txt') as f:
        print('I am going to sleep...', file=f)
        time.sleep(3)
    
    # works fine    
    with custom_logging('my_log.txt') as f:
        "dfgdfg" + 777
