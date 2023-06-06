# создание модели
from create_model import create_model
# дополнительные функции a(j,l), c(i,k,l) и т.д.
from sub_functions import SubFunctions
# выбор поля (спираль/решетка)
from select_field import select_field
# засекаем время работы решателя
import datetime

# массив для хранения переменных, содержащихся в подцикле (для последующего запрета этого подцикла)
all_loops_cons = list()  # массив ВСЕХ подциклов:
# [
#   {(i,j,k), ..., (i,j,k)}  - индексы фишек в 1-ом подцикле,
#   ...
#   {(i,j,k), ..., (i,j,k)}  - индексы фишек в s-ом подцикле,
# ]

# пользователь указывает количество фишек
n = int(input("Введите номер задачи для решения: "))
if n < 3:
    print("Невозможно решить задачу, т.к. количество фишек должно быть >= 3.")
    exit()
# создание экземпляра класса Дополнительных функций
sub_functions = SubFunctions(n)
# ищет все делители числа n, кроме делителя 1
lst_divisors = sub_functions.number_divisors(n)
# определяем, является ли поле спиралью и кол-во строк и столбцов в поле
is_spiral, chosen_field = select_field(lst_divisors)
# каждая фишка i имеет вид(рисунок линий) 1, 2, ..., 10; это значение выражает n_new
n_new = min([n, 10])  # см. С2'(версия с дубликатами)
# создаем модель решателя (model - модель, ans - 3х*массив из x_ijk, colors_list - 2x*массив из y_jl)
model, ans, colors_list = create_model("Tantrix", n, n_new, is_spiral, chosen_field)

# засекаем время работы решателя
d = datetime.datetime.now(datetime.timezone.utc)
temp_now = f'{d.hour+3}:{d.minute}:{d.second}.{d.microsecond}'

print("------------------- 1 ЗАПУСК РЕШАТЕЛЯ -------------------")
model.optimize()            # запуск решателя
sol = model.getBestSol()    # берем лучшее решение

print(f'\nВыбранное поле: {"Спираль" if is_spiral else "Решетка "+str(chosen_field[0])+"x"+str(chosen_field[1])}')

# вывод правильного расположения фишек (ответа)
vars_count = 0  # Кол-во переменных в текущем решении (число фишек в петле)
list_ans = list()  # двумерный массив вида [[i, j, k], ..., [i', j', k']], это индексы всех иксов (x_ijk в ответе)
for i in range(1, n_new + 1):
    for j in range(1, n + 1):
        for k in range(1, 7):
            try:
                if round(sol[ans[i - 1][j - 1][k - 1]], 1) == 1.0:
                    list_ans.append([i, j, k])
                    vars_count += 1
            except:
                print(f'Ответ:\nНе существует решения данной головоломки из {n} фишек на поле вида '
                      f'{"Спираль" if is_spiral else "Решетка "+str(chosen_field[0])+"x"+str(chosen_field[1])}')
                # засекаем время работы решателя
                d = datetime.datetime.now(datetime.timezone.utc)
                now = f'{d.hour + 3}:{d.minute}:{d.second}.{d.microsecond}'
                format = '%H:%M:%S.%f'
                time = str(datetime.datetime.strptime(now, format) - datetime.datetime.strptime(temp_now, format))[:-3]
                # print(f'{temp_now} -- начало')
                # print(f'{now} -- окончание')
                # print(f'{time} -- время решения')
                print(f'\nРешатель запускался 1 раз')
                exit()
# print(f"\nДвумерный массив вида [[i, j, k], ..., [i', j', k']], это индексы всех иксов (x_ijk в ответе)\n"
#       f"list_ans={list_ans}")
try:
    # хранит список всех петель за один запуск решателя
    loops = sub_functions.loops(list_ans, n_new, is_spiral, chosen_field)
except:
    print(f'Ответ:\nПревышено время ожидания. Не существует решения данной головоломки из {n} фишек на поле вида '
          f'{"Спираль" if is_spiral else "Решетка " + str(chosen_field[0]) + "x" + str(chosen_field[1])}')
    # засекаем время работы решателя
    d = datetime.datetime.now(datetime.timezone.utc)
    now = f'{d.hour + 3}:{d.minute}:{d.second}.{d.microsecond}'
    format = '%H:%M:%S.%f'
    time = str(datetime.datetime.strptime(now, format) - datetime.datetime.strptime(temp_now, format))[:-3]
    # print(f'{temp_now} -- начало')
    # print(f'{now} -- окончание')
    # print(f'{time} -- время решения')
    exit()

count_while = 1    # кол-во запусков решателя
while len(loops) != 1:
    count_while += 1
    print(f"\nКол-во переменных в текущем решении: {vars_count}")
    print(f"Обнаружено {len(loops)} подцикла => добавляем ограничение на подциклы.\n")
    # print(f'Подциклы на текущем запуске: loops={loops}')     # подциклы на текущем запуске
    for loop in loops:
        all_loops_cons.append(loop)  # найденные подциклы на текущем запуске добавили в общий массив всех подциклов

    # создаем вторую модель решателя (model - модель, ans - 3х*массив из x_ijk, colors_list - 2x*массив из y_jl)
    model, ans, colors_list = create_model("Tantrix", n, n_new, is_spiral, chosen_field)

    res_sum = 0  # для ограничения на подциклы, если они будут
    all_vars = model.getVars()  # получаем массив всех переменных модели

    for vars_in_loop in all_loops_cons:
        for var_in_loop in vars_in_loop:
            x = f'x_{var_in_loop[0]}_{var_in_loop[1]}_{var_in_loop[2]}'
            for var in all_vars:
                if x == str(var):  # если среди переменных нашлась переменная из подцикла
                    res_sum += var  # добавляем её в сумму, для последующего составления ограничения на подцикл

        model.addCons(res_sum <= (len(vars_in_loop) - 1))   # запрещаем каждый найденный подцикл
        res_sum = 0
    # print(f'ВСЕ ПОДЦИКЛЫ:\nall_loops_cons={all_loops_cons}')
    print(f"------------------- {count_while} ЗАПУСК РЕШАТЕЛЯ -------------------")
    # решение головоломки
    model.optimize()
    sol = model.getBestSol()  # берем лучшее решение

    # вывод правильного расположения фишек (ответа)
    vars_count = 0  # кол-во переменных в текущем решении (число фишек в петле)
    list_ans = list()  # двумерный массив вида [[i, j, k], ..., [i', j', k']], это индексы всех иксов (x_ijk в ответе)
    for i in range(1, n_new + 1):
        for j in range(1, n + 1):
            for k in range(1, 7):
                try:
                    if round(sol[ans[i - 1][j - 1][k - 1]], 1) == 1.0:
                        list_ans.append([i, j, k])
                        vars_count += 1
                except:
                    print(f'Ответ:\nНе существует решения данной головоломки из {n} фишек на поле вида '
                          f'{"Спираль" if is_spiral else "Решетка " + str(chosen_field[0]) + "x" + str(chosen_field[1])}')
                    # засекаем время работы решателя
                    d = datetime.datetime.now(datetime.timezone.utc)
                    now = f'{d.hour + 3}:{d.minute}:{d.second}.{d.microsecond}'
                    format = '%H:%M:%S.%f'
                    time = str(datetime.datetime.strptime(now, format) - datetime.datetime.strptime(temp_now, format))[
                           :-3]
                    # print(f'{temp_now} -- начало')
                    # print(f'{now} -- окончание')
                    # print(f'{time} -- время решения')
                    exit()

    # print(f'list_ans={list_ans}')

    # найденные петли за один запуск
    loops = sub_functions.loops(list_ans, n_new, is_spiral, chosen_field)
    # print(f'Подциклы на текущем запуске: loops={loops}')     # кол-во подциклов на текущем запуске
    # print(f'\nans={ans}')       # 3хмерный список всех переменных x_i_j_k
    # print(f'colors_list={colors_list}')   # 2хмерный список всех переменных y_j_l

    # чтобы избежать двойного вывода ответа(включая ветку else ниже) т.к. кол-во подциклов на перезапуске может меняться
    # и мы можем уйти в else
    # if len(loops) == 1:
    #     print(f'\nРешатель запускался {count_while} раз')
    #
    #     # засекаем время работы решателя
    #     d = datetime.datetime.now(datetime.timezone.utc)
    #     now = f'{d.hour + 3}:{d.minute}:{d.second}.{d.microsecond}'
    #     format = '%H:%M:%S.%f'
    #     time = str(datetime.datetime.strptime(now, format) - datetime.datetime.strptime(temp_now, format))[:-3]
    #     # print(f'{temp_now} -- начало')
    #     # print(f'{now} -- окончание')
    #     # print(f'{time} -- время решения')
    #     exit()

else:
    print(f"Кол-во переменных в текущем решении: {vars_count}")
    print("Ответ:")
    for i in range(1, n_new + 1):
        for j in range(1, n + 1):
            for k in range(1, 7):
                if round(sol[ans[i - 1][j - 1][k - 1]], 1) == 1.0:
                    # выводим ранее полученный ответ
                    print(f'x_{i}_{j}_{k}: {round(sol[ans[i - 1][j - 1][k - 1]], 1)}')
    # print(f'ans={ans}')     # 3хмерный список всех переменных x_i_j_k

print(f'\nРешатель запускался {count_while} раз')
# засекаем время работы решателя
d = datetime.datetime.now(datetime.timezone.utc)
now = f'{d.hour+3}:{d.minute}:{d.second}.{d.microsecond}'
format = '%H:%M:%S.%f'
time = str(datetime.datetime.strptime(now, format) - datetime.datetime.strptime(temp_now, format))[:-3]
# print(f'{temp_now} -- начало')
# print(f'{now} -- окончание')
# print(f'{time} -- время решения')
