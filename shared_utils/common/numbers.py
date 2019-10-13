

def get_plural(number, case1, case2, case5):
    if 11 <= number % 100 <= 19:
        return case5
    if number % 10 == 1:
        return case1
    if 2 <= number % 10 <= 4:
        return case2
    return case5


def prettify(value):
    suffixes = (
        ('B', 10 ** 9),
        ('M', 10 ** 6),
        ('k', 10 ** 3),
    )
    suffix = ''
    for suffix_key, suffix_value in suffixes:
        if value >= suffix_value:
            value /= suffix_value
            suffix = suffix_key
            break
    if value < 10:
        value = round(value, 1)
    else:
        value = int(round(value))
    return f'{value}{suffix}'
