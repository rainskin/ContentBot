def parse_hours_and_minutes(text: str):
    minutes = 0
    if ":" in text:
        hours, minutes = [parse_int(i) for i in text.split(":")]
    elif len(text) < 4:
        hours = parse_int(text)
    else:
        hours = parse_int(text[:-2])
        minutes = parse_int(text[-2:])

    if minutes > 59:
        raise ValueError('Неверное кол-во минут')

    return hours, minutes


def parse_int(text: str):
    try:
        return int(text)
    except ValueError:
        raise ValueError("В тексте должны быть только цифры")


def test():
    assert parse_hours_and_minutes("1") == (1, 0)
    assert parse_hours_and_minutes("12") == (12, 0)
    assert parse_hours_and_minutes("123") == (123, 0)
    assert parse_hours_and_minutes("1234") == (12, 34)
    assert parse_hours_and_minutes("12345") == (123, 45)
    assert parse_hours_and_minutes("1:2") == (1, 2)

    try:
        parse_hours_and_minutes("1m")
    except ValueError as e:
        assert str(e) == "В тексте должны быть только цифры"


test()
