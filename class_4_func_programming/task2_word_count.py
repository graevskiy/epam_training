# Task 2
# sentences = ['test string',​
#              'with two test words: test and test',​
#              'and some without ** string']​
# ​
# count = 0​
# for sentence in sentences:​
#     count += sentence.count('test')


# Написать в функциональном стиле функцию, которая на вход получает список строк и слово.
# Нужно вернуть количество вхождений этого слова в переданных строках.

from typing import List
from functools import reduce
from operator import add

def count_words(sentences: List[str], word: str) -> int:
    """ Counts number of `word` mentioned in all elements of
    `sentences` list

    :param sentences list: list of string where serach wil lbe done
    :param word str: word we are counting 
    
    :returns int: number of times it's found
    """
    return reduce(add, map(lambda x: x.count(word), sentences))