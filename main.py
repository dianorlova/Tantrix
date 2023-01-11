from pyscipopt import Model

model = Model("Tantrix")
# обозначения
# i - номер фишки               1 <= i <= n_new
# j - номер места на доске      1 <= j <= n
# k - ориентация фишки          1 <= k <= 6
# l - ребро места j             1 <= l <= 6

# количество фишек
with open('input.txt', 'r', encoding='utf-8') as file:
    n = int(file.read())

n_new = min([n, 10])  # см. С2'(версия с дубликатами)

ans = []


def create_x_i_j_k():
    """
    x_i_j_k = 1, если фишка i помещена на место j с ориентацией k
    x_i_j_k = 0, если фишка i не помещена на место j с ориентацией k
    """
    for i in range(1, n_new + 1):
        ans.append(list())
        for j in range(1, n + 1):
            ans[i - 1].append(list())
            for k in range(1, 7):
                ans[i - 1][j - 1].append(model.addVar(f"x_{i}_{j}_{k}", vtype="INTEGER"))


colors_list = []


def create_y_j_l():
    """
    Выражает цвет линии соответствующего ребра l места j
    y_j_l = 1
    y_j_l = 2
    y_j_l = 3 (обозначенный цвет)
    """
    for j in range(1, n + 1):
        colors_list.append(list())
        for l in range(1, 7):
            colors_list[j - 1].append(model.addVar(f"y_{j}_{l}", vtype="INTEGER"))


# a(j, l) – функция, которая возвращает номер места, смежного с местом j своим краем l,
#                 и возвращает 0, если такое место находится вне доски (т.е. нет соседей по ребру l для места j)

# neighbors_numbers_list = [] # Список номеров мест соседей для каждого места j и каждого ребра l
# for j in range(1, n + 1):
#     neighbors_numbers_list.append(list())
#     for l in range(1, 7):
#         neighbors_numbers_list[j - 1].append(model.addVar(f"a_{j}_{l}", vtype="INTEGER"))


def rest_1():
    """
    Ограничение C1: На каждое место кладется ровно 1 фишка
    """
    for j in range(1, n + 1):
        res_sum = 0
        for i in range(1, n_new + 1):
            for k in range(1, 7):
                res_sum += ans[i - 1][j - 1][k - 1]
                model.addCons(0 <= (ans[i - 1][j - 1][k - 1] <= 1))
        model.addCons(1 <= (res_sum <= 1))


def rest_2():
    """
    Ограничение C2': Каждая фишка i используется ровно оценка_сверху[(n+1-i)/10] раз
    """
    for i in range(1, n_new + 1):
        res_sum = 0
        for j in range(1, n + 1):
            for k in range(1, 7):
                res_sum += ans[i - 1][j - 1][k - 1]
                model.addCons(0 <= (ans[i - 1][j - 1][k - 1] <= 1))
        value = round((n + 1 - i) / 10)
        model.addCons(value <= (res_sum <= value))


# c(i, j, k) -функция, возвращает цвет(1,2 или 3) линии, соответствующей ребру l, когда фишка расположена в ориентации k
# y(j,l) - переменная выражает цвет линии соответствующего ребра l размещенной на месте j фишки
# def rest_3():
#     """
#     Ограничение C3: Линия обозначенного цвета любой из n фишек не может примыкать к границе доски размером n
#     """
#     for j in range(1, n + 1):
#         for l in range(1, 7):
            # если функция a(i,j,k) вернула 0:
                 # model.addCons(1 <= colors_list[j - 1][l - 1] <= 2)
            # иначе
                 # model.addCons(3 <= colors_list[j - 1][l - 1] <= 3)


create_x_i_j_k()
create_y_j_l()
rest_1()
rest_2()

model.optimize()
sol = model.getBestSol()  # берем лучшее решение
for i in range(1, n + 1):
    for j in range(1, n + 1):
        for k in range(1, 7):
            print("x_i_j_k: {}".format(sol[ans[i - 1][j - 1][k - 1]]))

file.close()
