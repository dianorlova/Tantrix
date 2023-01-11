from pyscipopt import Model

model = Model("Tantrix")

# количество фишек
with open('input.txt', 'r', encoding='utf-8') as file:
    n = int(file.read())

n_new = min([n, 10])  # см. С2'

# создание переменных
ans = []
for i in range(1, n_new + 1):
    ans.append(list())
    for j in range(1, n + 1):
        ans[i - 1].append(list())
        for k in range(1, 7):
            ans[i - 1][j - 1].append(model.addVar(f"x_{i}_{j}_{k}", vtype="INTEGER"))

neighbors_numbers_list = []
for j in range(1, n + 1):
    neighbors_numbers_list.append(list())
    for l in range(1, 7):
        neighbors_numbers_list[j - 1].append(model.addVar(f"a_{j}_{l}", vtype="INTEGER"))


# C1 - 'На каждое место кладется ровно 1 фишка' // res_sum должна = 1

def rest_1():
    for j in range(1, n + 1):
        res_sum = 0
        for i in range(1, n_new + 1):
            for k in range(1, 7):
                res_sum += ans[i - 1][j - 1][k - 1]
                model.addCons(0 <= (ans[i - 1][j - 1][k - 1] <= 1))
        model.addCons(1 <= (res_sum <= 1))


# C2' - 'Каждая фишка i используется ровно оценка_сверху[(n+1-i)/10] раз' // res_sum должна = оценка_сверху[(n+1-i)/10]
def rest_2():
    for i in range(1, n_new + 1):
        res_sum = 0
        for j in range(1, n + 1):
            for k in range(1, 7):
                res_sum += ans[i - 1][j - 1][k - 1]
                model.addCons(0 <= (ans[i - 1][j - 1][k - 1] <= 1))
        value = round((n + 1 - i) / 10)
        model.addCons(value <= (res_sum <= value))


# C3 - 'Линия обозначенного цвета любой из n фишек не может примыкать к границе доски размером n'
# c(i, j, k) возвращает цвет(1,2 или 3) линии, соответствующей ребру l, когда фишка расположена в ориентации k
# y(j,l) выражает цвет линии соответствующего ребра l размещенной на месте j фишки
def rest_3():
    for j in range(1, n + 1):
        for l in range(1, 7):

            model.addCons(0 <= neighbors_numbers_list[j-1][l-1] <= 0)
            # model.addCons(1 <= y[j-1][l-1] <= 2)


rest_1()
rest_2()

model.optimize()
sol = model.getBestSol()  # берем лучшее решение
for i in range(1, n + 1):
    for j in range(1, n + 1):
        for k in range(1, 7):
            print("x: {}".format(sol[ans[i - 1][j - 1][k - 1]]))

file.close()
