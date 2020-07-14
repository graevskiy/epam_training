import re

result = re.match(r'(P)(yt)hon', 'Python is the best')
print(result)  # <re.Match object; span=(0, 6), match='Python'>
print(result.group())  # Python
print(result.start())  # 0
print(result.end())  # 6

result = re.match(r'the', 'Python is the best')
print(result)  # None
