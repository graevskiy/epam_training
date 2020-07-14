import re

result = re.search(r'(\w*)th(\w*)', 'Python is the best')
print(result)  # <re.Match object; span=(0, 6), match='Python'>
print(result.group(0))  # Python
print(result.group(1))
print(result.group(2))
print(result.start())  # 0
print(result.end())  # 6
