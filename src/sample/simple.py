def add_one(number):
    if isinstance(number, str):
        number = int(number)
    return number + 1
