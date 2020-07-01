
import random
from memory_profiler import profile

@profile
def main():
    l = [random.randint(-255, 255) for _ in range(100000)]
    a = sorted(l)
    b = l.sort()
    
if __name__ == "__main__":
    main()
