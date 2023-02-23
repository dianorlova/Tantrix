from pyscipopt import Model

# главные ограничения C1-C4
from main_cons import MainConst
# дополнительные ограничения
from sub_cons import SubCons

# дополнительные функции a(j,l), c(i,k,l) и т.д.
from sub_functions import SubFunctions

# добавление переменных x_i_j_k и y_j_l
from create_vars import CreateVars

# создаёт структуру поля
from create_structure import create_structure


def create_model(model_name, n, n_new):
    # создаем модель решателя
    model = Model(model_name)
    ans = []  # ответ задачи Tantrix, список с иксами x_i_j_k
    colors_list = []  # список с игреками y_j_l

    # создаем обьект класса для создания переменных
    create_vars = CreateVars(n, n_new, ans, model, colors_list)
    # создаем переменную вида x_i_j_k
    create_vars.create_x_i_j_k()
    # создаем переменную вида y_j_l
    create_vars.create_y_j_l()

    # создаем обьект класса вспомогательных функций
    sub_functions = SubFunctions(n)

    # создаем обьект класса основных ограничений
    main_cons = MainConst(n, n_new, ans, model, colors_list)
    # создаем основные ограничения C1-C4
    main_cons.cons_1()
    main_cons.cons_2()
    # Из C3 и C4 следует, что любая линия обозначенного цвета должна быть частью петли,
    # т.е. они составляют необходимое и достаточное условие для того,
    # чтобы все линии обозначенного цвета образовывали петли.
    main_cons.cons_3(sub_functions)
    main_cons.cons_4(sub_functions)

    # создаем объект класса дополнительных ограничений
    sub_cons = SubCons(n, n_new, ans, model, colors_list)
    # создаем ограничение на цвета
    sub_cons.cons_colors(sub_functions)

    # записывает в файл координаты мест фишек на поле
    file = open('all_coordinates.txt', 'w', encoding='utf-8')
    file.write(f'{sub_functions.ans_to}')
    file.close()

    # создание и запись в файл структуры поля в виде графа
    create_structure(n, sub_functions)

    return model, ans, colors_list
