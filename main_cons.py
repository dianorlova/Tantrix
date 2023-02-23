import math


class MainConst:
    """
    Описывает основные ограничения C1-C4
    """
    def __init__(self, n, n_new, ans, model, colors_list):
        self.n = n
        self.n_new = n_new
        self.ans = ans
        self.model = model
        self.colors_list = colors_list

    def cons_1(self):
        """
        Ограничение C1: На каждое место кладется ровно 1 фишка
        """
        count_cons_1 = 0
        file = open('C1-output.txt', 'w', encoding='utf-8')
        for j in range(1, self.n + 1):
            res_sum = 0
            str = ''
            for i in range(1, self.n_new + 1):
                for k in range(1, 7):
                    res_sum += self.ans[i - 1][j - 1][k - 1]

                    # формируем вывод строчки (сумма x_i_j_k) при конкретном j
                    if i == k == 1:
                        str += f'{self.ans[i - 1][j - 1][k - 1]}'
                    else:
                        str += f' + {self.ans[i - 1][j - 1][k - 1]}'

            self.model.addCons(1 <= (res_sum <= 1))  # С1

            file.write(f'j={j}: {str} = 1\n')
            count_cons_1 += 1

        file.write(f'Ограничений C1: {count_cons_1}')
        file.close()

    def cons_2(self):
        """
        Ограничение C2': Каждая фишка i используется ровно оценка_сверху[(n+1-i)/10] раз
        """
        count_cons_2 = 0
        file = open('C2-output.txt', 'w', encoding='utf-8')
        for i in range(1, self.n_new + 1):
            res_sum = 0
            str = ''
            for j in range(1, self.n + 1):
                for k in range(1, 7):
                    res_sum += self.ans[i - 1][j - 1][k - 1]

                    # формируем вывод строчки (сумма x_i_j_k) при конкретном i
                    if j == k == 1:
                        str += f'{ self.ans[i - 1][j - 1][k - 1]}'
                    else:
                        str += f' + {self.ans[i - 1][j - 1][k - 1]}'

            value = math.ceil((self.n + 1 - i) / 10)
            self.model.addCons(value <= (res_sum <= value))  # C2

            file.write(f'i={i}: {str} = {value}\n')
            count_cons_2 += 1

        file.write(f'Ограничений C2: {count_cons_2}')
        file.close()

    # y(j,l) - переменная выражает цвет(1,2 или 3) линии соответствующего ребра l размещенной на месте j фишки
    # y(j,l) это colors_list[j - 1][l - 1]
    def cons_3(self, sub_functions):
        """
        Ограничение C3: Линия обозначенного цвета любой из n фишек не может примыкать к границе доски размером n
        """
        count_cons_3 = 0
        file = open('C3-output.txt', 'w', encoding='utf-8')
        for j in range(1, self.n + 1):
            for l in range(1, 7):
                if sub_functions.a(j, l) == 0:
                    self.model.addCons(1 <= (self.colors_list[j - 1][l - 1] <= 2))  # C3
                    # если у места j и его ребра l нет соседа, то цвет линии у этого ребра будет 1 или 2
                    # (т.е. НЕобозначенный цвет)
                    # P.s. Обозначенный цвет - тот, которым выстраивается петля среди всех фишек

                    file.write(f'1 <= {self.colors_list[j - 1][l - 1]} <= 2\n')
                    count_cons_3 += 1
        file.write(f'Ограничений C3: {count_cons_3}')
        file.close()


    def cons_4(self, sub_functions):
        """
            Ограничение C4: Соединение линий одного и того же цвета для каждых трех цветов.
            т.е. цвет линии на ребре l и места j должен соединяться с таким же цветом соседа j' по ребру l'
        """
        count_cons_4 = 0
        file = open('C4-output.txt', 'w', encoding='utf-8')
        for j in range(1, self.n + 1):
            for j1 in range(1, self.n + 1):
                for l in range(1, 7):
                    for l1 in range(1, 7):
                        if sub_functions.a(j, l) == j1 and sub_functions.a(j1, l1) == j:
                            y_j1_l1 = self.colors_list[j1 - 1][l1 - 1]

                            self.model.addCons(0 <= ((self.colors_list[j - 1][l - 1] - y_j1_l1) <= 0))  # C4: y_j_l = y_j'_l'
                            file.write(f'{self.colors_list[j - 1][l - 1]} = {y_j1_l1}\n')

                            count_cons_4 += 1
        file.write(f'Ограничений C4: {count_cons_4}')
        file.close()