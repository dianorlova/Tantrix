class SubCons:
    def __init__(self, n, n_new, ans, model, colors_list):
        self.n = n
        self.n_new = n_new
        self.ans = ans
        self.model = model
        self.colors_list = colors_list

    def cons_colors(self, sub_functions):
        """
        Дополнительное ограничение на цвета
        Принимает:
            sub_functions - объект класса SubFunctions
        """
        count_cons_5 = 0
        file = open('C_colors-output.txt', 'w', encoding='utf-8')
        for j in range(1, self.n + 1):
            for l in range(1, 7):
                res_sum = 0
                str = ''
                for i in range(1, self.n_new + 1):
                    for k in range(1, 7):
                        res_sum += sub_functions.c(i, k, l, self.n_new) * self.ans[i - 1][j - 1][k - 1]

                        if i == k == 1:
                            str += f'c_{i}_{k}_{l}*{self.ans[i - 1][j - 1][k - 1]}'
                        else:
                            str += f' + c_{i}_{k}_{l}*{self.ans[i - 1][j - 1][k - 1]}'

                self.model.addCons(0 <= (self.colors_list[j - 1][l - 1] - res_sum <= 0))

                file.write(f'j={j},l={l}: {str} = {self.colors_list[j - 1][l - 1]}\n')
                count_cons_5 += 1

        file.write(f'Ограничений C_colors: {count_cons_5}')
        file.close()

    # Оптимизация (Ограничения С7-С9) - убираем подциклы из 3, 4, 5 фишек при n>5
    def cons_7(self, is_spiral, chosen_field, sub_functions):
        """
            Убираем подциклы из 3 фишек для обозначенного цвета (т.е. убираем конкретные расположения конкретных фишек)
        """
        designated_color = sub_functions.get_designated_color(self.n_new)  # получение обозн. цвета (буква К, Ж или С)
        print(f'designated_color={designated_color}')
        # если обозначенный цвет красный (К)
        if designated_color == 'К':
            print("ОБОЗНАЧЕННЫЙ ЦВЕТ КРАСНЫЙ")
            for j in range(1, self.n + 1):
                sum1 = self.ans[2 - 1][j - 1][3 - 1] + self.ans[3 - 1][j - 1][5 - 1] + \
                       self.ans[2 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][5 - 1] + \
                       self.ans[3 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][1 - 1]
                self.model.addCons(sum1 <= 1)
                # Расшифровка: x_2_j_3 + x_3_j_5 + x_2_a(j,1)_5 + x_3_a(j,1)_1 <= 1          при j = 1,...,n

                sum2 = self.ans[2 - 1][j - 1][2 - 1] + self.ans[3 - 1][j - 1][4 - 1] + \
                       self.ans[2 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][6 - 1] + \
                       self.ans[3 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][2 - 1]
                self.model.addCons(sum2 <= 1)

                sum3 = self.ans[2 - 1][j - 1][1 - 1] + self.ans[3 - 1][j - 1][3 - 1] + \
                       self.ans[2 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][5 - 1] + \
                       self.ans[3 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][1 - 1]
                self.model.addCons(sum3 <= 1)

                sum4 = self.ans[2 - 1][j - 1][2 - 1] + self.ans[3 - 1][j - 1][4 - 1] + \
                       self.ans[2 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][4 - 1] + \
                       self.ans[3 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][6 - 1]
                self.model.addCons(sum4 <= 1)

                sum5 = self.ans[2 - 1][j - 1][1 - 1] + self.ans[3 - 1][j - 1][3 - 1] + \
                       self.ans[2 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][3 - 1] + \
                       self.ans[3 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][5 - 1]
                self.model.addCons(sum5 <= 1)

                sum6 = self.ans[2 - 1][j - 1][6 - 1] + self.ans[3 - 1][j - 1][2 - 1] + \
                       self.ans[2 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][4 - 1] + \
                       self.ans[3 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][6 - 1]
                self.model.addCons(sum6 <= 1)

        elif designated_color == 'Ж':
            print("ОБОЗНАЧЕННЫЙ ЦВЕТ ЖЕЛТЫЙ")

        elif designated_color == 'С':
            print("ОБОЗНАЧЕННЫЙ ЦВЕТ СИНИЙ")
        else:
            print("ЧТО-ТО ПОШЛО НЕ ТАК. НЕ НАШЁЛСЯ ОБОЗНАЧЕННЫЙ ЦВЕТ")
