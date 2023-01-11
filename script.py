# количество фишек
with open('input.txt', 'r', encoding='utf-8') as file:
    n = int(file.read())

# определяем обозначенный цвет
dict_colors = {'yellow': [1, 2, 3, 9], 'red': [4, 5, 7], 'blue': [6, 8, 10]}
def check_designated_color():
    designated_color = 'red'    # по умолчанию
    for key, value in dict_colors.items():
        if n % 10 in value:
            designated_color = key
            # print(f'Обозначенный цвет: {designated_color}')
    return designated_color

check_designated_color()

def x(i, j, k):
    # if :
    #     return False
    return True


# C1 - 'На каждое место кладется ровно 1 фишка' // res_sum должна = 1
for j in range(1, n + 1):
    res_sum = 0
    for i in range(1, n + 1):
        for k in range(1, 7):
            res_sum = res_sum + x(i, j, k)

# C2' - 'Каждая фишка i используется ровно оценка_сверху[(n+1-i)/10] раз' // res_sum должна = оценка_сверху[(n+1-i)/10]
n_new = min([n, 10])
for i in range(1, n + 1):
    res_sum = 0
    for j in range(1, n + 1):
        for k in range(1, 7):
            res_sum = res_sum + x(i, j, k)

# C3 - 'Линия обозначенного цвета любой из n фишек не может примыкать к границе доски размером n'
# c(i, j, k) возвращает цвет(1,2 или 3) линии, соответствующей ребру l, когда фишка расположена в ориентации k

# def c(i, k, l):
#     if color=="red":



# y(j,l) выражает цвет линии соответствующего ребра l размещенной на месте j фишки
def y(j,l):
    res_sum = 0
    for j in range(1, n + 1):
        for l in range(1, 7):
            for i in range(1, n + 1):
                for k in range(1, 7):
                    res_sum = res_sum + c(i, k, l)*x(i, j, k)
    return res_sum

file.close()
