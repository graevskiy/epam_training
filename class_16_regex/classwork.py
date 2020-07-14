import re

r_str = r'\b[a-zA-Z]{2}'

pattern = re.compile(r_str)

word = "word1 word woro!"

res = re.findall(r'\b[a-zA-Z]{2}', word)

print(res)
# print(res.group())

