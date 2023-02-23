from create_model import create_model

# дополнительные функции a(j,l), c(i,k,l) и т.д.
from sub_functions import SubFunctions

# массив для хранения пременных, содержащихся в подцикле
loops_cons = list()

# читаем из файла количество фишек
file = open('input.txt', 'r', encoding='utf-8')
n = int(file.read())
file.close()

sub_functions = SubFunctions(n)

n_new = min([n, 10])  # см. С2'(версия с дубликатами)

model, ans, colors_list = create_model("Tantrix", n, n_new)

# решение головоломки
model.optimize()
sol = model.getBestSol()  # берем лучшее решение

# вывод правильного расположения фишек (ответа)
vars_count = 0   # Кол-во переменных в текущем решении (число фишек в петле)
list_ans = list()
for i in range(1, n_new + 1):
    for j in range(1, n + 1):
        for k in range(1, 7):
            if sol[ans[i - 1][j - 1][k - 1]] == 1.0:
                list_ans.append([i, j, k])
                vars_count += 1

# ф-ия f возвращает массив с информацией о переменных, которые содержатся в петле
vars_in_loop = sub_functions.get_vars_in_loop(list_ans, 3, n_new)
print(vars_in_loop)
if len(vars_in_loop) != n:
    # чтобы хранить все ограничения на подциклы для каждой итерации запуска решателя
    # если длина массива с информацией о петле меньше n
    # сохранить этот массив с информацией в общем массиве loops_cons
    loops_cons.append(vars_in_loop)
    print(f"Кол-во переменных в текущем решении: {vars_count}")
    print("Количество переменных маловато для ответа, добавляем ограничение на подциклы")

    model, ans, colors_list = create_model("Tantrix", n, n_new)

    res_sum = 0  # для ограничения на подциклы, если они будут
    all_vars = model.getVars()
    for var in all_vars:
        for var_in_loop in vars_in_loop:
            x = f'x_{var_in_loop[0]}_{var_in_loop[1]}_{var_in_loop[2]}'
            if x == str(var):
                res_sum += var
    print(res_sum)

    model.addCons(res_sum <= (len(vars_in_loop) - 1))
    print("Ограничение на подциклы добавили")

    # решение головоломки
    model.optimize()
    sol = model.getBestSol()  # берем лучшее решение

    # вывод правильного расположения фишек (ответа)
    vars_count = 0  # Кол-во переменных в текущем решении (число фишек в петле)
    list_ans = list()
    for i in range(1, n_new + 1):
        for j in range(1, n + 1):
            for k in range(1, 7):
                if sol[ans[i - 1][j - 1][k - 1]] == 1.0:
                    print(f'x_{i}_{j}_{k}: {sol[ans[i - 1][j - 1][k - 1]]}')
                    list_ans.append([i, j, k])
                    vars_count += 1

    # ф-ия f возвращает массив с информацией о переменных, которые содержатся в петле
    vars_in_loop = sub_functions.get_vars_in_loop(list_ans, 3, n_new)
    print(vars_in_loop)

    print(f'ans={ans}')
    print(f'res_sum={res_sum}')  # не хочет выводить res_sum (ограничение на подцикл)

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
