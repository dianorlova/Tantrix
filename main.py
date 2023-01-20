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
                model.addCons(0 <= (ans[i - 1][j - 1][k - 1] <= 1))  # x_i_j_k принимает значение 1 или 0

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
            model.addCons(1 <= (colors_list[j - 1][l - 1] <= 3))  # y_j_l принимает значение 1, 2 или 3

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
                # model.addCons(0 <= (ans[i - 1][j - 1][k - 1] <= 1))  # x_i_j_k принимает значение 1 или 0
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
                # model.addCons(0 <= (ans[i - 1][j - 1][k - 1] <= 1))  # x_i_j_k принимает значение 1 или 0
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


create_x_i_j_k()
create_y_j_l()
cons_1()
cons_2()

# Показывает шаг, на который нужно сместиться по выбранному ребру с текущего места, чтобы перейти на новое место
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


def find_all_coordinates(n):
    """
    Возвращает:
    Словарь ans_to с номерами мест и их координатами на доске,
    Словарь ans_from, аналог ans_to, ключ-значение поменяны местами.
    """
    sp_num = 1  # номер шага в спирали (или номер ячейки на поле)
    start = (0, 0)
    ans_to = {}  # словарь, где 'ключ' - номер места(от 1 до n), 'значение' - координаты этого места на доске
    ans_from = {}  # аналогично, но 'ключ' и 'значение' поменяны местами (для удобства)
    i = 1
    while True:
        # l проходит по всем рёбрам в спирали
        for l in ([6] * max(0, i - 2) + [1] * (i - 1) + [2] * (i - 1) + [3] * (i - 1) + [4] * (i - 1) + [5] * i):
            if sp_num > n:
                return ans_to, ans_from
            ans_to[sp_num] = start
            ans_from[start] = sp_num
            sp_num += 1
            start = bias(start, l)
        i += 1


ans_to, ans_from = find_all_coordinates(n)
file = open('all_coordinates.txt', 'w', encoding='utf-8')
file.write(f'{ans_to}')
file.close()


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


# y(j,l) - переменная выражает цвет(1,2 или 3) линии соответствующего ребра l размещенной на месте j фишки
def cons_3():
    """
    Ограничение C3: Линия обозначенного цвета любой из n фишек не может примыкать к границе доски размером n
    """
    count_cons_3 = 0
    file = open('C3-output.txt', 'w', encoding='utf-8')
    for j in range(1, n + 1):
        for l in range(1, 7):
            if a(j, l) == 0:
                model.addCons(1 <= (colors_list[j - 1][l - 1] <= 2))  # C3
                # если у места j и его ребра l нет соседа, то цвет линии у этого ребра будет 1 или 2
                # (т.е. НЕобозначенный цвет)
                # P.s. Обозначенный цвет - тот, которым выстраивается петля среди всех фишек

                file.write(f'1 <= {colors_list[j - 1][l - 1]} <= 2\n')
                count_cons_3 += 1
    file.write(f'Ограничений C3: {count_cons_3}')
    file.close()


def cons_4():
    """
        Ограничение C4: Соединение линий одного и того же цвета для каждых трех цветов.
        т.е. цвет линии на ребре l и места j должен соединяться с таким же цветом соседа j' по ребру l'
    """
    count_cons_4 = 0
    file = open('C4-output.txt', 'w', encoding='utf-8')
    for j in range(1, n + 1):
        for j1 in range(1, n + 1):
            for l in range(1, 7):
                for l1 in range(1, 7):
                    if a(j, l) == j1 and a(j1, l1) == j:
                        y_j1_l1 = colors_list[j1 - 1][l1 - 1]
                        # model.addCons(y_j1_l1 <= (colors_list[j - 1][l - 1] <= y_j1_l1))  # C4
                        model.addCons(0 <= ((colors_list[j - 1][l - 1] - y_j1_l1) <= 0))  # C4: y_j_l = y_j'_l'
                        file.write(f'{colors_list[j - 1][l - 1]} = {y_j1_l1}\n')

                        count_cons_4 += 1
    file.write(f'Ограничений C4: {count_cons_4}')
    file.close()


# Из C3 и C4 следует, что любая линия обозначенного цвета должна быть частью петли,
# т.е. они составляют необходимое и достаточное условие для того,
# чтобы все линии обозначенного цвета образовывали петли.
cons_3()
cons_4()
graph = {}


def create_structure():
    """
    Создаёт следующую структуру(словарь) данных:
    {Ячейка 1:
       {Ребро 1:Номер соседа, ..., Ребро 6:Номер соседа},
     Ячейка 2:{...},
     ...,
     Ячейка n:{...}}
    """
    file = open('graph.txt', 'w', encoding='utf-8')
    file.write(f'{{\n')  # экранируем '{' путём удвоения

    graph.fromkeys(list(range(1, n + 1)))  # заполняем словарь ключами - номерами ячеек(мест)
    for i in range(1, n + 1):
        dict_rib_neighbor = {}  # словарь ребро-сосед
        graph[i] = dict_rib_neighbor.fromkeys(
            list(range(1, 7)))  # для каждой ячейки есть свой словарь с ребрами-соседями
        for l in range(1, 7):
            dict_rib_neighbor[l] = a(i, l)  # ребро(ключ): сосед(значение)
            graph[i][l] = dict_rib_neighbor[l]

        file.write(f'\t{i}:\n\t\t{graph[i]}\n')

    file.write(f'}}')  # экранируем '}' путём удвоения
    file.close()


create_structure()

model.optimize()
sol = model.getBestSol()  # берем лучшее решение
for i in range(1, n_new + 1):
    for j in range(1, n + 1):
        for k in range(1, 7):
            print(f'x_{i}_{j}_{k}: {sol[ans[i - 1][j - 1][k - 1]]}')

for j in range(1, n + 1):
    for l in range(1, 7):
        print(f'y_{j}_{l}: {sol[colors_list[j - 1][l - 1]]}')