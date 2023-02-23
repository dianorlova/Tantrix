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

# создаем модель решателя
model = Model("Tantrix")
# обозначения
# i - номер фишки               1 <= i <= n_new
# j - номер места на доске      1 <= j <= n
# k - ориентация фишки          1 <= k <= 6
# l - ребро места j             1 <= l <= 6

# читаем из файла количество фишек
file = open('input.txt', 'r', encoding='utf-8')
n = int(file.read())
file.close()

n_new = min([n, 10])  # см. С2'(версия с дубликатами)

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

# записывает в файл координаты мест фишек на поле
file = open('all_coordinates.txt', 'w', encoding='utf-8')
file.write(f'{sub_functions.ans_to}')
file.close()

# создаем объект класса дополнительных ограничений
sub_cons = SubCons(n, n_new, ans, model, colors_list)
# создаем ограничение на цвета
sub_cons.cons_colors(sub_functions)

# создание и запись в файл структуры поля в виде графа
create_structure(n, sub_functions)

# решение головоломки
model.optimize()
sol = model.getBestSol()  # берем лучшее решение

# вывод правильного расположения фишек (ответа)
vars_count = 0   # Кол-во переменных в текущем решении (число фишек в петле)
res_sum = 0     # для ограничения на подциклы, если они будут
for i in range(1, n_new + 1):
    for j in range(1, n + 1):
        for k in range(1, 7):
            if sol[ans[i - 1][j - 1][k - 1]] == 1.0:
                vars_count += 1
                res_sum += ans[i - 1][j - 1][k - 1]     # для ограничения на подциклы, если они будут
                # print(f'x_{i}_{j}_{k}: {sol[ans[i - 1][j - 1][k - 1]]}')  # раньше выводили здесь ответ

print(f'res_sum={res_sum}')
if vars_count != n:
    print(f"Кол-во переменных в текущем решении: {vars_count}")
    print("Количество переменных маловато для ответа, добавляем ограничение на подциклы")

# ******** ПЫТАЮСЬ НОВУЮ МОДЕЛЬ СДЕЛАТЬ
    model = Model("NewTantrix")

    ans = []  # ответ задачи Tantrix, список с иксами x_i_j_k
    colors_list = []  # список с игреками y_j_l

    # создаем объект класса для создания переменных
    create_vars = CreateVars(n, n_new, ans, model, colors_list)

    # создаем переменную вида x_i_j_k
    create_vars.create_x_i_j_k()
    # создаем переменную вида y_j_l
    create_vars.create_y_j_l()

    # создаем объект класса основных ограничений
    main_cons = MainConst(n, n_new, ans, model, colors_list)
    # создаем основные ограничения C1-C4
    main_cons.cons_1()
    main_cons.cons_2()
    # Из C3 и C4 следует, что любая линия обозначенного цвета должна быть частью петли,
    # т.е. они составляют необходимое и достаточное условие для того,
    # чтобы все линии обозначенного цвета образовывали петли.
    main_cons.cons_3(sub_functions)
    main_cons.cons_4(sub_functions)
    # model.addCons(res_sum <= (vars_count - 1))              # ДОБАВЛЯЮ ОГРАНИЧЕНИЕ НА ПОДЦИКЛЫ ЧУТЬ ПОРАНЬШЕ

    # записывает в файл координаты мест фишек на поле
    file = open('all_coordinates.txt', 'w', encoding='utf-8')
    file.write(f'{sub_functions.ans_to}')
    file.close()
    print(f'res_sum={res_sum}')

    # создаем объект класса дополнительных ограничений
    sub_cons = SubCons(n, n_new, ans, model, colors_list)
    # создаем ограничение на цвета
    sub_cons.cons_colors(sub_functions)
    print("Мы тут1")
    # print(f'res_sum={res_sum}')                                     # НЕ ВЫВОДИТСЯ
    print("Мы тут2")                                                # НЕ ВЫВОДИТСЯ ЕСЛИ НЕ УБРАТЬ СТРОЧКУ ВЫШЕ
    # создание и запись в файл структуры поля в виде графа
    create_structure(n, sub_functions)
    print("Мы тут3")
    # ********

    # model.addCons(res_sum <= (vars_count - 1))
    print("Ограничение на подциклы добавили")

                                                                    # ДАЛЬШЕ НИЧЕГО НЕ ПРОИСХОДИТ
    # решение головоломки (перезапускаем решатель)
    model.optimize()
    sol = model.getBestSol()  # берем лучшее решение
    for i in range(1, n_new + 1):
        for j in range(1, n + 1):
            for k in range(1, 7):
                if sol[ans[i - 1][j - 1][k - 1]] == 1.0:
                    print(f'x_{i}_{j}_{k}: {sol[ans[i - 1][j - 1][k - 1]]}')
    print(f'ans={ans}')
    print(f'res_sum={res_sum}')                                     # не хочет выводить res_sum (ограничение на подцикл)

else:
    print(f"Кол-во переменных в текущем решении: {vars_count}")

    for i in range(1, n_new + 1):
        for j in range(1, n + 1):
            for k in range(1, 7):
                if sol[ans[i - 1][j - 1][k - 1]] == 1.0:
                    # выводим ранее полученный ответ
                    print(f'x_{i}_{j}_{k}: {sol[ans[i - 1][j - 1][k - 1]]}')
    print("Всё ОК")



# вывод цвета для ребра l места j
# for j in range(1, n + 1):
#     for l in range(1, 7):
#         print(f'y_{j}_{l}: {sol[colors_list[j - 1][l - 1]]}')
