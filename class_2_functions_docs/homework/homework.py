# Task
# Есть список словарей: ​
# ​
# ​ 
# friends = [​​​
#     {'name': 'Сэм', 'gender': 'Мужской', 'sport': 'Баскетбол'}, ​​
#     {'name': 'Эмили', 'gender': 'Женский' 'sport': 'Волейбол'}, ​​​
#     …​​​
# ]​
# ​
# Напишите функции для работы с массивами данных (стабы уже написаны).
# ​
# Пример работы программы:​
 
# result = query(​​​
#     friends,​​​
#     select('name', 'gender', 'sport'),​​​
#     field_filter('sport', ['Баскетбол', 'Волейбол']),​​​
#     field_filter('gender', ['Мужской']),​​​
# )

# Требуется возможность из списка диктов выбрать интересуюшие нас колонки и фильтрануть данные по ним.

# Не забываем документацию!


from functools import wraps
from typing import List, Dict, Any, Set, Tuple, Sequence


def itemgetter_iterable(*items: Any) -> callable:
    """ This is a copy of itemgetter from operator module.
    https://docs.python.org/3/library/operator.html#operator.itemgetter
    with the exception it returns tuple even if len(items) == 1

    :param items: Is used as identifiers of item to get from an object
    :type items: Any type accepted by the operand’s __getitem__() method
    Dictionaries accept any hashable value. 
    Lists, tuples, and strings accept an index or a slice
    
    :returns: function to call on an object you wish to get element(s) from
    :rtype: function
    """

    def g(obj: Any) -> Tuple[Any]:
        """ Function replicates inner function from 
        https://docs.python.org/3/library/operator.html#operator.itemgetter

        :param obj: An object to operate on
        :type obj: Any object supporting __getitem__() method

        :returns: tuple of values of an object per each item
        :rtype: tuple
        """

        return tuple(obj[item] for item in items)
    return g


def select(*field_names: str) -> Tuple[Tuple[str], callable]:
    """ Wrapper function providing clean interface.
    Specifies keys needed to be selected from the data.
    Defines and returns another fuction with interface unified with
    other functions being used in a query.
    
    :param field_names: only fields to include in output data
    Can be empty, considering all fields are needed to return
    :type field_names: str

    :returns: function to invoke for selection with unified interface
    :rtype: function
    """

    @wraps(select)
    def inner_select(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """ Internal function of 'select' which manipulates data
        by selecting appropriate fields only and dporring the rest

        :param data: List of dicts, same structure that passed to 'query'.
        Hence all items are consistent with field names (no missing fields)
        :type data: List of dicts. Replicates structure of input data (param data)

        :returns: subset of input data. Same rows but reducing fields
        to only those which listed in outer function in param field_names
        :rtype: List of dicts. Replicates structure of input data (param data)
        """

        res = []
        # Iterating through list items
        for row in data:
            # in case some parameters passed, grab for each of them
            # appropriate values by itemgetter_iterable
            # pushing field_names (sequence of keys) and 
            # values we get (sequence of values) to zip to create
            # source for dict
            if field_names:                
                res += [dict(zip(
                    field_names, 
                    itemgetter_iterable(*field_names)(row)
                ))]
            # Easy part - no fileds means take whole dict as is
            else:
                res += [row]
        return res
    return inner_select


def field_filter(field_name: str, *values: str) -> Tuple[str, callable]:
    """ Function takes filter constraints by specifying field-value(s)
    associations and applies to the data. Implements 'OR' logic through
    elements of param values.

    :param field_name: field name to apply filter on.
    Hence exists in query (param data). Case sensitive.
    :type field_name: str

    :param values: List of values for given field (param field_name)
    :type values: list

    :returns: function with unified interface to call it for actual filtering
    from 'query'
    :rtype: function
    """

    @wraps(field_filter)
    def inner_filter(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """ Internal function of 'field_filter' which filteres data
        by selecting dropping items which don't satisfy a filter constraints

        :param data: List of dicts, same structure that passed to 'query'.
        Hence all items are consistent with field names (no missing fields)
        :type data: List of dicts. Replicates structure of input data (param data)

        :returns: subset of input data. Same fields but drops rows which don't
        satisfy a give constraint
        :rtype: List of dicts. Replicates structure of input data (param data)
        """

        res = []
        for row in data:
            if row[field_name] in values:
                res += [row]
        return res
    return inner_filter


def query(
        data: List[Dict[str, Any]], 
        selection: callable,
        *filters: callable
    ) -> List[Dict[str, Any]]:
    """ This function filters given data according to 
    passed parameters.
    Implemented as a convener of filters followed by select.
    filters appy in a given order and implement logic 'And'.
    So filtered data in the output is the only records
    which satisfy all filters.

    :param data: The data to to filter
    :type data: List of dicts. Each dict keys (aka fields) and values
    are strings. May have unpredictable behavior if values have other types
    
    :param selection: Sets constraints on fields to select from the data
    :type selection: function which has to be invoked with the data
    passed to it.
    
    :param filters: Set of filters to apply to the data consecutively.
    :type filters: functions

    :returns: Filtered data (by applied filters) 
    with only specified fields (according to select). Order of fields
    matches with order of parameters in param selection.
    :rtype: List of dicts. Replicates structure of input data (param data)
    """

    # Sanity check that input is not empty
    if not data:
        return []

    # Looping through filters followed by select
    # Don't realize how to do an opposite way because in that case 
    # data can miss keys which may be used later in filters.
    res = data
    for f in filters + (selection,):
        res = f(res)
    return res


