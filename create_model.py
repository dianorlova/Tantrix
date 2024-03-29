from pyscipopt import Model

# главные ограничения C1-C4
from main_cons import MainConst
# дополнительные ограничения
from sub_cons import SubCons
# дополнительные функции a(j,l), c(i,k,l) и т.д.
from sub_functions import SubFunctions
# добавление переменных x_ijk и y_jl
from create_vars import CreateVars
# создание структуры спирального поля (для проверки)
from create_structure import create_structure


def create_model(model_name, n, n_new, is_spiral, chosen_field):
    """
    Принимает:
        model_name - название модели,
        n - количество фишек
        n_new - количество видов фишек (всего может быть 10 видов, т.е. рисунков)
        is_spiral - является ли поле спиралью
        chosen_field - кол-во строк и столбцов в поле ((0,0) для спирали)

    Возвращает:
        model - модель решателя,
        ans - 3х*массив из x_ijk,
        colors_list - 2x*массив из y_jl
    """
    # создаем модель решателя
    model = Model(model_name)
    # устанавливаем лимит 10 минут на время запуска
    model.setParam('limits/time', 600)
    ans = []  # ответ задачи Tantrix, список с иксами x_i_j_k
    colors_list = []  # список с игреками y_j_l

    # создаем объект класса для создания переменных
    create_vars = CreateVars(n, n_new, ans, model, colors_list)
    # создаем переменную вида x_i_j_k
    create_vars.create_x_i_j_k()
    # создаем переменную вида y_j_l
    create_vars.create_y_j_l()

    # создаем объект класса вспомогательных функций
    sub_functions = SubFunctions(n)

    # создаем объект класса основных ограничений
    main_cons = MainConst(n, n_new, ans, model, colors_list, is_spiral, chosen_field)
    # создаем основные ограничения C1-C4
    main_cons.cons_1()
    main_cons.cons_2()
    main_cons.cons_3(sub_functions)
    main_cons.cons_4(sub_functions)

    # создаем объект класса дополнительных ограничений
    sub_cons = SubCons(n, n_new, ans, model, colors_list)
    # создаем ограничение на цвета
    sub_cons.cons_colors(sub_functions)

    # записывает в файл координаты мест фишек на спиральной форме поля (для проверки)
    # file = open('all_coordinates.txt', 'w', encoding='utf-8')
    # file.write(f'{sub_functions.ans_to}')
    # file.close()

    # создание и запись в файл структуры спирального поля в виде графа (для проверки)
    # create_structure(n, sub_functions)

    # добавление оптимизации
    if n > 5:
        sub_cons.cons_7(is_spiral, chosen_field, sub_functions)     # убираем подциклы из 3 фишек
        sub_cons.cons_8(is_spiral, chosen_field, sub_functions)     # убираем подциклы из 4 фишек
        sub_cons.cons_9(is_spiral, chosen_field, sub_functions)     # убираем подциклы из 5 фишек

    return model, ans, colors_list
