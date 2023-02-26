# создание модели
from create_model import create_model
# дополнительные функции a(j,l), c(i,k,l) и т.д.
from sub_functions import SubFunctions

# массив для хранения переменных, содержащихся в подцикле (для последующего запрета этого подцикла)
loops_cons = list()     # массив вида:
# [
#   [[i,j,k], ..., [i,j,k]]  - индексы фишек в 1-ом подцикле,
#   ...
#   [[i,j,k], ..., [i,j,k]]  - индексы фишек в s-ом подцикле,
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

# каждая фишка i имеет вид(рисунок линий) 1, 2, ..., 10; это значение выражает n_new
n_new = min([n, 10])  # см. С2'(версия с дубликатами)

# создаем модель решателя (model - модель, ans - 3х*массив из x_ijk, colors_list - 2x*массив из y_jl
model, ans, colors_list = create_model("Tantrix", n, n_new)

# решение головоломки
model.optimize()
sol = model.getBestSol()  # берем лучшее решение
print("------------------------------------------ПЕРВЫЙ ЗАПУСК РЕШАТЕЛЯ--------------------------------------------")

# вывод правильного расположения фишек (ответа)
vars_count = 0   # Кол-во переменных в текущем решении (число фишек в петле)
list_ans = list()   # двумерный массив вида [[i, j, k], ..., [i', j', k']], это индексы всех иксов (x_ijk в ответе)
for i in range(1, n_new + 1):
    for j in range(1, n + 1):
        for k in range(1, 7):
            if sol[ans[i - 1][j - 1][k - 1]] == 1.0:
                list_ans.append([i, j, k])
                vars_count += 1

print(f"\nДвумерный массив вида [[i, j, k], ..., [i', j', k']], это индексы всех иксов (x_ijk в ответе)\n"
      f"list_ans={list_ans}")

# ф-ия get_vars_in_loop возвращает массив с информацией о переменных, которые содержатся в петле
vars_in_loop = sub_functions.get_vars_in_loop(list_ans, 3, n_new,list_ans[0])
print(f"\nМассив вида [[i,j,k], ..., [i',j',k']], где ijk - индексы переменных в петле/подцикле"
      f" после 1-го запуска решателя:\nvars_in_loop={vars_in_loop}")

# все петли
loops = sub_functions.loops(list_ans, 3, n_new)
print(f'loops={loops}')

# if len(vars_in_loop) != n:
if len(loops) != 1:
    # чтобы хранить все ограничения на подциклы для каждой итерации запуска решателя
    # если длина массива с информацией о петле меньше n
    # сохранить этот массив с информацией в общем массиве loops_cons
    loops_cons.append(vars_in_loop)
    print(f"\nКол-во переменных в текущем решении: {vars_count}")
    print("!! Обнаружены подциклы => добавляем ограничение на подциклы !!")

    # создаем вторую модель решателя (model - модель, ans - 3х*массив из x_ijk, colors_list - 2x*массив из y_jl
    model, ans, colors_list = create_model("Tantrix", n, n_new)

    res_sum = 0  # для ограничения на подциклы, если они будут
    all_vars = model.getVars()  # получаем массив всех переменных модели
    for var in all_vars:
        for var_in_loop in vars_in_loop:
            x = f'x_{var_in_loop[0]}_{var_in_loop[1]}_{var_in_loop[2]}'
            if x == str(var):   # если среди переменных нашлась переменная из подцикла
                res_sum += var  # добавляем её в сумму, для последующего составления ограничения на подцикл
    print(f'res_sum={res_sum}')

    model.addCons(res_sum <= (len(vars_in_loop) - 1))
    print("Ограничение на подцикл добавили")
    print("------------------------------------------------------------------------------------------------------")

    # решение головоломки
    model.optimize()
    sol = model.getBestSol()  # берем лучшее решение
    print("------------------------------------------ВТОРОЙ ЗАПУСК РЕШАТЕЛЯ-------------------------------------------")

    # вывод правильного расположения фишек (ответа)
    vars_count = 0  # кол-во переменных в текущем решении (число фишек в петле)
    list_ans = list()   # двумерный массив вида [[i, j, k], ..., [i', j', k']], это индексы всех иксов (x_ijk в ответе)
    for i in range(1, n_new + 1):
        for j in range(1, n + 1):
            for k in range(1, 7):
                if sol[ans[i - 1][j - 1][k - 1]] == 1.0:
                    print(f'x_{i}_{j}_{k}: {sol[ans[i - 1][j - 1][k - 1]]}')
                    list_ans.append([i, j, k])
                    vars_count += 1

    # ф-ия get_vars_in_loop возвращает массив с информацией о переменных, которые содержатся в петле
    vars_in_loop = sub_functions.get_vars_in_loop(list_ans, 3, n_new, list_ans[0])
    print(f"\nМассив вида [[i,j,k], ..., [i',j',k']], где ijk - индексы переменных в петле/подцикле"
          f" после 2-го запуска решателя:\nvars_in_loop={vars_in_loop}")

    # все петли
    loops = sub_functions.loops(list_ans, 3, n_new)
    print(f'loops={loops}')

    print(f'\nans={ans}')
    print(f'colors_list={colors_list}')

else:
    print(f"Кол-во переменных в текущем решении: {vars_count}")

    for i in range(1, n_new + 1):
        for j in range(1, n + 1):
            for k in range(1, 7):
                if sol[ans[i - 1][j - 1][k - 1]] == 1.0:
                    # выводим ранее полученный ответ
                    print(f'x_{i}_{j}_{k}: {sol[ans[i - 1][j - 1][k - 1]]}')
    print(f'ans={ans}')
    print("Всё ОК")
