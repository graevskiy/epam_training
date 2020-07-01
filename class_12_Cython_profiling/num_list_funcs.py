
import random
from memory_profiler import profile

@profile
def filter_list(l):
    c = [x for x in l if x > 0]
    a = filter(lambda x: x > 0, l)
    b = list(filter(lambda x: x > 0, l))
    del c, b
    return a

if __name__ == "__main__":
    l = [random.randint(-255, 255) for _ in range(100000)]
    filter_list(l)
