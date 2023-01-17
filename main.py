from pyscipopt import Model
import math

model = Model("Tantrix")
# обозначения
# i - номер фишки               1 <= i <= n_new
# j - номер места на доске      1 <= j <= n
# k - ориентация фишки          1 <= k <= 6
# l - ребро места j             1 <= l <= 6

# количество фишек
file = open('input.txt', 'r', encoding='utf-8')
n = int(file.read())
file.close()

n_new = min([n, 10])  # см. С2'(версия с дубликатами)

ans = []


def create_x_i_j_k():
    """
    x_i_j_k = 1, если фишка i помещена на место j с ориентацией k,
    x_i_j_k = 0, если фишка i не помещена на место j с ориентацией k
    """
    count_x_i_j_k = 0
    file = open('x_i_j_k-output.txt', 'w', encoding='utf-8')
    for i in range(1, n_new + 1):
        ans.append(list())
        for j in range(1, n + 1):
            ans[i - 1].append(list())
            for k in range(1, 7):
                ans[i - 1][j - 1].append(model.addVar(f"x_{i}_{j}_{k}", vtype="INTEGER"))
                count_x_i_j_k += 1
                file.write(f'{ans[i - 1][j - 1][k - 1]}\n')
    file.write(f'Переменных x_i_j_k: {count_x_i_j_k}')
    file.close()


colors_list = []


def create_y_j_l():
    """
    Выражает цвет линии соответствующего ребра l места j,
    y_j_l = 1,
    y_j_l = 2,
    y_j_l = 3 (обозначенный цвет)
    """
    count_y_j_l = 0
    file = open('y_j_l-output.txt', 'w', encoding='utf-8')
    for j in range(1, n + 1):
        colors_list.append(list())
        for l in range(1, 7):
            colors_list[j - 1].append(model.addVar(f"y_{j}_{l}", vtype="INTEGER"))
            count_y_j_l += 1
            file.write(f'{colors_list[j - 1][l - 1]}\n')

    file.write(f'Переменных y_j_l: {count_y_j_l}')
    file.close()


# a(j, l) – функция, которая возвращает номер места, смежного с местом j своим краем l,
#                 и возвращает 0, если такое место находится вне доски (т.е. нет соседей по ребру l для места j)

# neighbors_numbers_list = [] # Список номеров мест соседей для каждого места j и каждого ребра l

def cons_1():
    """
    Ограничение C1: На каждое место кладется ровно 1 фишка
    """
    count_cons_1 = 0
    file = open('C1-output.txt', 'w', encoding='utf-8')
    for j in range(1, n + 1):
        res_sum = 0
        str = ''
        for i in range(1, n_new + 1):
            for k in range(1, 7):
                res_sum += ans[i - 1][j - 1][k - 1]
                model.addCons(0 <= (ans[i - 1][j - 1][k - 1] <= 1))  # x_i_j_k принимает значение 1 или 0
                # формируем вывод строчки (сумма x_i_j_k) при конкретном j
                if i == k == 1:
                    str += f'{ans[i - 1][j - 1][k - 1]}'
                else:
                    str += f' + {ans[i - 1][j - 1][k - 1]}'

        model.addCons(1 <= (res_sum <= 1))  # С1
        file.write(f'j={j}: {str} = 1\n')
        count_cons_1 += 1

    file.write(f'Ограничений C1: {count_cons_1}')
    file.close()


def cons_2():
    """
    Ограничение C2': Каждая фишка i используется ровно оценка_сверху[(n+1-i)/10] раз
    """
    count_cons_2 = 0
    file = open('C2-output.txt', 'w', encoding='utf-8')
    for i in range(1, n_new + 1):
        res_sum = 0
        str = ''
        for j in range(1, n + 1):
            for k in range(1, 7):
                res_sum += ans[i - 1][j - 1][k - 1]
                model.addCons(0 <= (ans[i - 1][j - 1][k - 1] <= 1))  # x_i_j_k принимает значение 1 или 0
                # строка 102 дублируется в C1, так что можно её убрать
                # формируем вывод строчки (сумма x_i_j_k) при конкретном i
                if j == k == 1:
                    str += f'{ans[i - 1][j - 1][k - 1]}'
                else:
                    str += f' + {ans[i - 1][j - 1][k - 1]}'

        value = math.ceil((n + 1 - i) / 10)
        model.addCons(value <= (res_sum <= value))  # C2
        file.write(f'i={i}: {str} = {value}\n')
        count_cons_2 += 1

    file.write(f'Ограничений C2: {count_cons_2}')
    file.close()


# y(j,l) - переменная выражает цвет линии соответствующего ребра l размещенной на месте j фишки
# def cons_3():
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
cons_1()
cons_2()

# graph = {
#     {'Ячейка 1': [4, 5, 6, 7, 2, 3],
#      'Ячейка 2': [],
#      # ...
#      'Ячейка n': []
#      }
# }


# показывает шаг, на который нужно сместиться по выбранному ребру с текущего места, чтобы перейти на новое место
# см. картинку https://github.com/stephanh42/hexutil/blob/master/img/hexcoords.png
step = {
    1: (2, 0),
    2: (1, 1),
    3: (-1, 1),
    4: (-2, 0),
    5: (-1, -1),
    6: (1, -1)
}


def bias(current_location, l):
    """
    Вычисление координат нового места, на которое сместились по ребру l

    Принимает:
        current_location - номер текущего места,
        l - номер ребра текущего места

    Возвращает:
        Координаты нового места, на которое сместились по ребру l
    """
    x, y = current_location
    dx, dy = step[l]
    return x + dx, y + dy


def disk(n):
    sp_num = 1      # номер шага в спирали
    start = (0, 0)
    ans_to = {}     # словарь, где 'ключ' - номер места(от 1 до n), 'значение' - координаты этого места на доске
    ans_from = {}   # аналогично, но 'ключ' и 'значение' поменяны местами
    i = 1
    while True:
        for l in ([6] * max(0, i - 2) + [1] * (i - 1) + [2] * (i - 1) + [3] * (i - 1) + [4] * (i - 1) + [5] * i):
            if sp_num > n:
                return ans_to, ans_from
            ans_to[sp_num] = start
            ans_from[start] = sp_num
            sp_num += 1
            start = bias(start, l)
        i += 1


ans_to, ans_from = disk(n)


# print(ans_from.get(__a(ans_to[35],3),0))
print(ans_to)
print(ans_from)
# print(a(ans_to[35],3))


def a(j, l):
    """
    Принимает:
        j - номер текущего места,
        l - номер ребра текущего места
    Возвращает:
        Номер места(соседа), смежного с местом j своим краем l,
         и возвращает 0, если такое место находится вне доски.
    """
    return ans_from.get(bias(ans_to[j], l), 0)


# print(a(7,3)) => 18
# для места 7 и его ребра 3 есть сосед по этому ребру с местом 18 (см.картинку со спиралью)

model.optimize()
sol = model.getBestSol()  # берем лучшее решение
# for i in range(1, n + 1):
#     for j in range(1, n + 1):
#         for k in range(1, 7):
#             print(f'x_{i}_{j}_{k}: {sol[ans[i - 1][j - 1][k - 1]]}')
