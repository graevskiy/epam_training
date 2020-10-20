# file: bar.py

import foo

foo.func()  # Здесь будет AttributeError

def get_message():
    return 'Hello from bar.py!'
