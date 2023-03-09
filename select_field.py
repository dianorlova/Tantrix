def create_field_list(lst_divisors):
    """Функция создает и возвращает строку с возможными вариантами полей"""
    fields = "0. Спиральное поле\n"
    for index, divisor in enumerate(lst_divisors):
        fields += f"{index+1}. Сетка из {divisor[0]} строк и {divisor[1]} столбцов\n"
    fields += f"{len(lst_divisors)+1}. Выход"
    return fields


def select_field(lst_divisors):
    """
    Функция предлагает пользователю выбрать поле и возвращает кортеж,
    где is_spiral - True/False - является ли поле спиралью,
    и кортеж с кол-вом строк и столбцов в поле ((0, 0) для спирали)
    """
    print(create_field_list(lst_divisors))
    is_spiral = False
    chosen_field = int(input("Выберите поле для решения головоломки, введя соответсвующий номер: "))
    if chosen_field >= len(lst_divisors)+1:
        exit()
    if chosen_field == 0:
        is_spiral = True
        return is_spiral, (0, 0)
    return is_spiral, lst_divisors[chosen_field-1]
