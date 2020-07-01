
from memory_profiler import profile

@profile
def track_dict_set():
    dict_plain = {}
    for i in range(1000, 10000):
        dict_plain[i] = i**10

    dict_set = {}
    for i in range(1000, 10000):
        dict_set.setdefault(i, i**10)

    dict_upd = {}
    for i in range(1000, 10000):
        dict_upd.update({i: i**10})

if __name__ == "__main__":
    track_dict_set()
