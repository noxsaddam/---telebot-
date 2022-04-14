from collections import OrderedDict


def para(pull):
    return list(OrderedDict.fromkeys([i for i in pull if pull.count(i) == 2]))


def two_pairs(pull):
    value = list(OrderedDict.fromkeys([i for i in pull if pull.count(i) == 2]))
    return value if len(value) == 2 else False


def sets(pull):
    return list(OrderedDict.fromkeys([i for i in pull if pull.count(i) == 3]))


def full_house(pull):
    value = list(OrderedDict.fromkeys(sets(pull) + para(pull)))
    return value if len(value) == 2 and [i for i in value if pull.count(i) == 3] else False


def kare(pull):
    return list(OrderedDict.fromkeys([i for i in pull if pull.count(i) == 4]))


def street(pull):
    for value_cards in (('2', '3', '4', '5', '6', '7', '8', '9', '10', 'В', 'Д', 'К', 'А'),
                        ('А', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'В', 'Д', 'К')):

        pull = sorted(pull, key=lambda x: value_cards.index(x))
        index_pull = [value_cards.index(i) for i in pull]
        # check = [index_pull[i + 1] for i in range(len(index_pull) - 1) if index_pull[i + 1] - 1 == index_pull[i]]
        count = 1
        for i in range(len(index_pull) - 1):
            if index_pull[i] == index_pull[i + 1] - 1:
                count += 1
                if count == 5:
                    return True
            else:
                count = 1
    return False


def flash(pull_suit):
    suit = {"Ч": "Черви", "Б": "Буби", "К": "Крести", "В": "Вини"}
    res = list(OrderedDict.fromkeys([i for i in pull_suit if pull_suit.count(i) >= 5]))
    return suit["".join(res)] if res else False


def street_flash(pull, pull_suit):
    return all((flash(pull_suit), street(pull)))


def flash_royal(pull, pull_suit):
    v = [i for i in range(len(pull)) if pull[i] in ("К", 'А')]
    if flash(pull_suit):
        check = True if [pull_suit[i] == flash(pull_suit)[0] for i in v].count(True) >= 2 else False
        return True if all([i in pull for i in ['10', 'В', 'Д', 'К', 'А']])\
                       and street_flash(pull, pull_suit) \
                       and check else False
    return False


def combination(cards, cards_table=[]):
    cards_value = [i[:-1].upper() for i in cards]
    cards_table_value = [i[:-1].upper() for i in cards_table]
    pull = cards_value + cards_table_value
    pull_suit = [i[-1].upper() for i in cards] + [i[-1].upper() for i in cards_table]

    if flash_royal(pull, pull_suit):
        return f'Да ты везунчик!У тебя Флеш Рояль!'

    elif street_flash(pull, pull_suit):
        return f"Вау! У тебя Стрит Флеш!"

    elif kare(pull):
        return f"У тебя Каре - {kare(pull)[0]}"

    elif full_house(pull):
        return f"У тебя Фулл Хаус из {full_house(pull)[0]} и {full_house(pull)[1]}"

    elif flash(pull_suit):
        return f"У тебя Флеш - {flash(pull_suit)}"

    elif street(pull):
        return f"У тебя Стрит"

    elif sets(pull):
        return f"У тебя Сет - {sets(pull)[0]}"

    elif two_pairs(pull):
        return f"У тебя Две Пары - {two_pairs(pull)[0]} и {two_pairs(pull)[1]}"

    elif para(pull):
        if cards_value[0] == cards_value[1]:
            return f"У тебя карманная пара - {cards_value[0]}"
        return f"У тебя Пара {para(pull)[0]}"

    return f"Не нашел кобминаций"


# def output_combinations():
#     return f"Вероятность Пары: {}\nВероятность Сета: {}\nВероятность Каре: {}\nВероятность Фулл хауса: {}\n

# cards = input("Карманные карты?").split()
#
# stage = input("Стадия игры?")
#
# if stage == "pref":
#     print(para(cards)) if para(cards) else None
# elif stage == "flop":
#     cards_table = input("Введите 3 карты со стола").split()
#     # cards_value = [i[:-1] for i in cards]
#     # cards_table_value = [i[:-1] for i in cards_table]
#     # pull = cards_value + cards_table_value
#     print(combination(cards,cards_table))
# elif stage == "tern":
#     cards_table = input("Введите 4 карты со стола").split()
#
# print(combination(['Кч', '8ч', 'Вч', 'Дч', '9ч', '10ч', 'Ав']))
