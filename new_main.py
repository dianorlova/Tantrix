# создание модели
from create_model import create_model
# дополнительные функции a(j,l), c(i,k,l) и т.д.
from sub_functions import SubFunctions

# массив для хранения переменных, содержащихся в подцикле (для последующего запрета этого подцикла)
all_loops_cons = list()  # массив ВСЕХ подциклов:
# [
#   {(i,j,k), ..., (i,j,k)}  - индексы фишек в 1-ом подцикле,
#   ...
#   {(i,j,k), ..., (i,j,k)}  - индексы фишек в s-ом подцикле,
# ]

# читаем из файла количество фишек
file = open('input.txt', 'r', encoding='utf-8')
n = int(file.read())
file.close()
if n < 3:
    print("Нет решения. Количество фишек должно быть <=3 .")
    exit()

# создание экземпляра класса Дополнительных функций
sub_functions = SubFunctions(n)

# ищет все делители числа n, кроме делителя 1
lst_divisors = sub_functions.number_divisors(n)
print(lst_divisors)

# каждая фишка i имеет вид(рисунок линий) 1, 2, ..., 10; это значение выражает n_new
n_new = min([n, 10])  # см. С2'(версия с дубликатами)

# создаем модель решателя (model - модель, ans - 3х*массив из x_ijk, colors_list - 2x*массив из y_jl
model, ans, colors_list = create_model("Tantrix", n, n_new)

# решение головоломки
model.optimize()
sol = model.getBestSol()  # берем лучшее решение
print("------------------------------------------ 1 ЗАПУСК РЕШАТЕЛЯ --------------------------------------------")

# вывод правильного расположения фишек (ответа)
vars_count = 0  # Кол-во переменных в текущем решении (число фишек в петле)
list_ans = list()  # двумерный массив вида [[i, j, k], ..., [i', j', k']], это индексы всех иксов (x_ijk в ответе)
for i in range(1, n_new + 1):
    for j in range(1, n + 1):
        for k in range(1, 7):
            if round(sol[ans[i - 1][j - 1][k - 1]], 1) == 1.0:
                list_ans.append([i, j, k])
                vars_count += 1

print(f"\nДвумерный массив вида [[i, j, k], ..., [i', j', k']], это индексы всех иксов (x_ijk в ответе)\n"
      f"list_ans={list_ans}")

# хранит список всех петель за один запуск решателя
loops = sub_functions.loops(list_ans, n_new)

count_while = 0
while len(loops) != 1:
    count_while += 1
    print(f"\nКол-во переменных в текущем решении: {vars_count}")
    print(f"!! Обнаружено {len(loops)} подцикла => добавляем ограничение на подциклы !!")
    print(f'loops={loops}')
    for loop in loops:
        all_loops_cons.append(loop)  # найденные подциклы добавили в общий массив всех подциклов

    # создаем вторую модель решателя (model - модель, ans - 3х*массив из x_ijk, colors_list - 2x*массив из y_jl
    model, ans, colors_list = create_model("Tantrix", n, n_new)

    res_sum = 0  # для ограничения на подциклы, если они будут
    all_vars = model.getVars()  # получаем массив всех переменных модели

    for vars_in_loop in all_loops_cons:  # было for vars_in_loop in loops:
        for var_in_loop in vars_in_loop:
            x = f'x_{var_in_loop[0]}_{var_in_loop[1]}_{var_in_loop[2]}'
            for var in all_vars:
                if x == str(var):  # если среди переменных нашлась переменная из подцикла
                    res_sum += var  # добавляем её в сумму, для последующего составления ограничения на подцикл

        model.addCons(res_sum <= (len(vars_in_loop) - 1))
        res_sum = 0

    print(f'ВСЕ ПОДЦИКЛЫ:\nall_loops_cons={all_loops_cons}')
    print("Ограничение на подцикл(ы) добавили")

    # решение головоломки
    model.optimize()
    sol = model.getBestSol()  # берем лучшее решение
    print(f"---------------------------------------- {count_while+1} ЗАПУСК РЕШАТЕЛЯ -----------------------------------------")
    print(f'Решатель перезапускался {count_while} раз')
    # вывод правильного расположения фишек (ответа)
    vars_count = 0  # кол-во переменных в текущем решении (число фишек в петле)
    list_ans = list()  # двумерный массив вида [[i, j, k], ..., [i', j', k']], это индексы всех иксов (x_ijk в ответе)
    for i in range(1, n_new + 1):
        for j in range(1, n + 1):
            for k in range(1, 7):
                # print(f'x_{i}_{j}_{k}: {round(sol[ans[i - 1][j - 1][k - 1]],1)}')
                if round(sol[ans[i - 1][j - 1][k - 1]], 1) == 1.0:
                    print(f'x_{i}_{j}_{k}: {round(sol[ans[i - 1][j - 1][k - 1]], 1)}')
                    list_ans.append([i, j, k])
                    vars_count += 1

    # все петли
    print(f'list_ans={list_ans}')
    loops = sub_functions.loops(list_ans, n_new)
    print(f'loops={loops}')
    print(f'\nans={ans}')
    print(f'colors_list={colors_list}')
else:
    print(f"Кол-во переменных в текущем решении: {vars_count}")
    for i in range(1, n_new + 1):
        for j in range(1, n + 1):
            for k in range(1, 7):
                if round(sol[ans[i - 1][j - 1][k - 1]], 1) == 1.0:
                    # выводим ранее полученный ответ
                    print(f'x_{i}_{j}_{k}: {round(sol[ans[i - 1][j - 1][k - 1]], 1)}')
    print(f'ans={ans}')
    print("Всё ОК")

# print("***********")
# print(f'a_2(11,1,4)={sub_functions.a_2(11,1,4)} должно быть 12')
# print(f'a_2(11,6,4)={sub_functions.a_2(11,6,4)} должно быть 7')
# print(f'a_2(11,4,4)={sub_functions.a_2(11,4,4)} должно быть 10')
