import dis

x = 0

def incr():
    global x
    x += 1


dis.dis(incr)