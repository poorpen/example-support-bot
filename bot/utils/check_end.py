import re


def check_float_end(number: float, end: str):
    """
    number: float передаем число
    end: str передаем в виде строки, так как для проверки будем использовать модуль re
    """
    pattern = end
    check = re.search(pattern, str(number))
    if check:
        return int(number)
    else:
        return number

