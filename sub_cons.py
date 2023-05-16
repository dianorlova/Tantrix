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
        # print(f'designated_color={designated_color}')
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
            for j in range(1, self.n + 1):
                sum1 = self.ans[1 - 1][j - 1][6 - 1] + self.ans[2 - 1][j - 1][6 - 1] + \
                       self.ans[2 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][2 - 1] + \
                       self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][2 - 1]
                self.model.addCons(sum1 <= 1)

                sum2 = self.ans[1 - 1][j - 1][6 - 1] + self.ans[3 - 1][j - 1][1 - 1] + \
                       self.ans[3 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][3 - 1] + \
                       self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][2 - 1]
                self.model.addCons(sum2 <= 1)

                sum3 = self.ans[1 - 1][j - 1][6 - 1] + self.ans[5 - 1][j - 1][3 - 1] + \
                       self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][5 - 1] + \
                       self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][2 - 1]
                self.model.addCons(sum3 <= 1)

                sum5 = self.ans[2 - 1][j - 1][6 - 1] + self.ans[3 - 1][j - 1][1 - 1] + \
                       self.ans[3 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][3 - 1] + \
                       self.ans[2 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][2 - 1]
                self.model.addCons(sum5 <= 1)

                sum6 = self.ans[2 - 1][j - 1][6 - 1] + self.ans[5 - 1][j - 1][3 - 1] + \
                       self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][5 - 1] + \
                       self.ans[2 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][2 - 1]
                self.model.addCons(sum6 <= 1)

                sum8 = self.ans[3 - 1][j - 1][1 - 1] + self.ans[5 - 1][j - 1][3 - 1] + \
                       self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][5 - 1] + \
                       self.ans[3 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][3 - 1]
                self.model.addCons(sum8 <= 1)

                sum11 = self.ans[1 - 1][j - 1][5 - 1] + self.ans[2 - 1][j - 1][5 - 1] + \
                        self.ans[2 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][3 - 1] + \
                        self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][3 - 1]
                self.model.addCons(sum11 <= 1)

                sum12 = self.ans[1 - 1][j - 1][5 - 1] + self.ans[3 - 1][j - 1][6 - 1] + \
                        self.ans[3 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][4 - 1] + \
                        self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][3 - 1]
                self.model.addCons(sum12 <= 1)

                sum13 = self.ans[1 - 1][j - 1][5 - 1] + self.ans[5 - 1][j - 1][2 - 1] + \
                        self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][6 - 1] + \
                        self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][3 - 1]
                self.model.addCons(sum13 <= 1)

                sum15 = self.ans[2 - 1][j - 1][5 - 1] + self.ans[3 - 1][j - 1][6 - 1] + \
                        self.ans[3 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][4 - 1] + \
                        self.ans[2 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][3 - 1]
                self.model.addCons(sum15 <= 1)

                sum16 = self.ans[2 - 1][j - 1][5 - 1] + self.ans[5 - 1][j - 1][2 - 1] + \
                        self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][6 - 1] + \
                        self.ans[2 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][3 - 1]
                self.model.addCons(sum16 <= 1)

                sum18 = self.ans[3 - 1][j - 1][6 - 1] + self.ans[5 - 1][j - 1][2 - 1] + \
                        self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][6 - 1] + \
                        self.ans[3 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][4 - 1]
                self.model.addCons(sum18 <= 1)

                sum21 = self.ans[1 - 1][j - 1][4 - 1] + self.ans[2 - 1][j - 1][4 - 1] + \
                        self.ans[2 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][2 - 1] + \
                        self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][2 - 1]
                self.model.addCons(sum21 <= 1)

                sum22 = self.ans[1 - 1][j - 1][4 - 1] + self.ans[3 - 1][j - 1][5 - 1] + \
                        self.ans[3 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][3 - 1] + \
                        self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][2 - 1]
                self.model.addCons(sum22 <= 1)

                sum23 = self.ans[1 - 1][j - 1][4 - 1] + self.ans[5 - 1][j - 1][1 - 1] + \
                        self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][5 - 1] + \
                        self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][2 - 1]
                self.model.addCons(sum23 <= 1)

                sum25 = self.ans[2 - 1][j - 1][4 - 1] + self.ans[3 - 1][j - 1][5 - 1] + \
                        self.ans[3 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][3 - 1] + \
                        self.ans[2 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][2 - 1]
                self.model.addCons(sum25 <= 1)

                sum26 = self.ans[2 - 1][j - 1][4 - 1] + self.ans[5 - 1][j - 1][1 - 1] + \
                        self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][5 - 1] + \
                        self.ans[2 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][2 - 1]
                self.model.addCons(sum26 <= 1)

                sum28 = self.ans[3 - 1][j - 1][5 - 1] + self.ans[5 - 1][j - 1][1 - 1] + \
                        self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][5 - 1] + \
                        self.ans[3 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][3 - 1]
                self.model.addCons(sum28 <= 1)

                sum31 = self.ans[1 - 1][j - 1][5 - 1] + self.ans[2 - 1][j - 1][5 - 1] + \
                        self.ans[2 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][1 - 1] + \
                        self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][1 - 1]
                self.model.addCons(sum31 <= 1)

                sum32 = self.ans[1 - 1][j - 1][5 - 1] + self.ans[3 - 1][j - 1][6 - 1] + \
                        self.ans[3 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][2 - 1] + \
                        self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][1 - 1]
                self.model.addCons(sum32 <= 1)

                sum33 = self.ans[1 - 1][j - 1][5 - 1] + self.ans[5 - 1][j - 1][2 - 1] + \
                        self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][4 - 1] + \
                        self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][1 - 1]
                self.model.addCons(sum33 <= 1)

                sum35 = self.ans[2 - 1][j - 1][5 - 1] + self.ans[3 - 1][j - 1][6 - 1] + \
                        self.ans[3 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][2 - 1] + \
                        self.ans[2 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][1 - 1]
                self.model.addCons(sum35 <= 1)

                sum36 = self.ans[2 - 1][j - 1][5 - 1] + self.ans[5 - 1][j - 1][2 - 1] + \
                        self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][4 - 1] + \
                        self.ans[2 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][1 - 1]
                self.model.addCons(sum36 <= 1)

                sum38 = self.ans[3 - 1][j - 1][6 - 1] + self.ans[5 - 1][j - 1][2 - 1] + \
                        self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][4 - 1] + \
                        self.ans[3 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][2 - 1]
                self.model.addCons(sum38 <= 1)

                sum41 = self.ans[1 - 1][j - 1][4 - 1] + self.ans[2 - 1][j - 1][4 - 1] + \
                        self.ans[2 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][6 - 1] + \
                        self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][6 - 1]
                self.model.addCons(sum41 <= 1)

                sum42 = self.ans[1 - 1][j - 1][4 - 1] + self.ans[3 - 1][j - 1][5 - 1] + \
                        self.ans[3 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][1 - 1] + \
                        self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][6 - 1]
                self.model.addCons(sum42 <= 1)

                sum43 = self.ans[1 - 1][j - 1][4 - 1] + self.ans[5 - 1][j - 1][1 - 1] + \
                        self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][3 - 1] + \
                        self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][6 - 1]
                self.model.addCons(sum43 <= 1)

                sum45 = self.ans[2 - 1][j - 1][4 - 1] + self.ans[3 - 1][j - 1][5 - 1] + \
                        self.ans[3 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][1 - 1] + \
                        self.ans[2 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][6 - 1]
                self.model.addCons(sum45 <= 1)

                sum46 = self.ans[2 - 1][j - 1][4 - 1] + self.ans[5 - 1][j - 1][1 - 1] + \
                        self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][3 - 1] + \
                        self.ans[2 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][6 - 1]
                self.model.addCons(sum46 <= 1)

                sum48 = self.ans[3 - 1][j - 1][5 - 1] + self.ans[5 - 1][j - 1][1 - 1] + \
                        self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][3 - 1] + \
                        self.ans[3 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][1 - 1]
                self.model.addCons(sum48 <= 1)

                sum51 = self.ans[1 - 1][j - 1][3 - 1] + self.ans[2 - 1][j - 1][3 - 1] + \
                        self.ans[2 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][1 - 1] + \
                        self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][1 - 1]
                self.model.addCons(sum51 <= 1)

                sum52 = self.ans[1 - 1][j - 1][3 - 1] + self.ans[3 - 1][j - 1][4 - 1] + \
                        self.ans[3 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][2 - 1] + \
                        self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][1 - 1]
                self.model.addCons(sum52 <= 1)

                sum53 = self.ans[1 - 1][j - 1][3 - 1] + self.ans[5 - 1][j - 1][6 - 1] + \
                        self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][4 - 1] + \
                        self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][1 - 1]
                self.model.addCons(sum53 <= 1)

                sum55 = self.ans[2 - 1][j - 1][3 - 1] + self.ans[3 - 1][j - 1][4 - 1] + \
                        self.ans[3 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][2 - 1] + \
                        self.ans[2 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][1 - 1]
                self.model.addCons(sum55 <= 1)

                sum56 = self.ans[2 - 1][j - 1][3 - 1] + self.ans[5 - 1][j - 1][6 - 1] + \
                        self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][4 - 1] + \
                        self.ans[2 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][1 - 1]
                self.model.addCons(sum56 <= 1)

                sum58 = self.ans[3 - 1][j - 1][4 - 1] + self.ans[5 - 1][j - 1][6 - 1] + \
                        self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][4 - 1] + \
                        self.ans[3 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][2 - 1]
                self.model.addCons(sum58 <= 1)

                if len(self.ans) >= 10:  # т.к. в ограничениях есть фишка вида 10 (а фишек может быть всего 9)
                    sum4 = self.ans[1 - 1][j - 1][6 - 1] + self.ans[10 - 1][j - 1][6 - 1] + \
                           self.ans[10 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               2 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][2 - 1]
                    self.model.addCons(sum4 <= 1)

                    sum7 = self.ans[2 - 1][j - 1][6 - 1] + self.ans[10 - 1][j - 1][6 - 1] + \
                           self.ans[10 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               2 - 1] + \
                           self.ans[2 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][2 - 1]
                    self.model.addCons(sum7 <= 1)

                    sum9 = self.ans[3 - 1][j - 1][1 - 1] + self.ans[10 - 1][j - 1][6 - 1] + \
                           self.ans[10 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               2 - 1] + \
                           self.ans[3 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][3 - 1]
                    self.model.addCons(sum9 <= 1)

                    sum10 = self.ans[5 - 1][j - 1][3 - 1] + self.ans[10 - 1][j - 1][6 - 1] + \
                            self.ans[10 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                                2 - 1] + \
                            self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                                5 - 1]
                    self.model.addCons(sum10 <= 1)

                    sum14 = self.ans[1 - 1][j - 1][5 - 1] + self.ans[10 - 1][j - 1][5 - 1] + \
                            self.ans[10 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                                3 - 1] + \
                            self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                                3 - 1]
                    self.model.addCons(sum14 <= 1)

                    sum17 = self.ans[2 - 1][j - 1][5 - 1] + self.ans[10 - 1][j - 1][5 - 1] + \
                            self.ans[10 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                                3 - 1] + \
                            self.ans[2 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                                3 - 1]
                    self.model.addCons(sum17 <= 1)

                    sum19 = self.ans[3 - 1][j - 1][6 - 1] + self.ans[10 - 1][j - 1][5 - 1] + \
                            self.ans[10 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                                3 - 1] + \
                            self.ans[3 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                                4 - 1]
                    self.model.addCons(sum19 <= 1)

                    sum20 = self.ans[5 - 1][j - 1][2 - 1] + self.ans[10 - 1][j - 1][5 - 1] + \
                            self.ans[10 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                                3 - 1] + \
                            self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                                6 - 1]
                    self.model.addCons(sum20 <= 1)

                    sum24 = self.ans[1 - 1][j - 1][4 - 1] + self.ans[10 - 1][j - 1][4 - 1] + \
                            self.ans[10 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                                2 - 1] + \
                            self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                                2 - 1]
                    self.model.addCons(sum24 <= 1)

                    sum27 = self.ans[2 - 1][j - 1][4 - 1] + self.ans[10 - 1][j - 1][4 - 1] + \
                            self.ans[10 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                                2 - 1] + \
                            self.ans[2 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                                2 - 1]
                    self.model.addCons(sum27 <= 1)

                    sum29 = self.ans[3 - 1][j - 1][5 - 1] + self.ans[10 - 1][j - 1][4 - 1] + \
                            self.ans[10 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                                2 - 1] + \
                            self.ans[3 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                                3 - 1]
                    self.model.addCons(sum29 <= 1)

                    sum30 = self.ans[5 - 1][j - 1][1 - 1] + self.ans[10 - 1][j - 1][4 - 1] + \
                            self.ans[10 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                                2 - 1] + \
                            self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                                5 - 1]
                    self.model.addCons(sum30 <= 1)

                    sum34 = self.ans[1 - 1][j - 1][5 - 1] + self.ans[10 - 1][j - 1][5 - 1] + \
                            self.ans[10 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                                1 - 1] + \
                            self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                                1 - 1]
                    self.model.addCons(sum34 <= 1)

                    sum37 = self.ans[2 - 1][j - 1][5 - 1] + self.ans[10 - 1][j - 1][5 - 1] + \
                            self.ans[10 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                                1 - 1] + \
                            self.ans[2 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                                1 - 1]
                    self.model.addCons(sum37 <= 1)

                    sum39 = self.ans[3 - 1][j - 1][6 - 1] + self.ans[10 - 1][j - 1][5 - 1] + \
                            self.ans[10 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                                1 - 1] + \
                            self.ans[3 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                                2 - 1]
                    self.model.addCons(sum39 <= 1)

                    sum40 = self.ans[5 - 1][j - 1][2 - 1] + self.ans[10 - 1][j - 1][5 - 1] + \
                            self.ans[10 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                                1 - 1] + \
                            self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                                4 - 1]
                    self.model.addCons(sum40 <= 1)

                    sum44 = self.ans[1 - 1][j - 1][4 - 1] + self.ans[10 - 1][j - 1][4 - 1] + \
                            self.ans[10 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                                6 - 1] + \
                            self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                                6 - 1]
                    self.model.addCons(sum44 <= 1)

                    sum47 = self.ans[2 - 1][j - 1][4 - 1] + self.ans[10 - 1][j - 1][4 - 1] + \
                            self.ans[10 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                                6 - 1] + \
                            self.ans[2 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                                6 - 1]
                    self.model.addCons(sum47 <= 1)

                    sum49 = self.ans[3 - 1][j - 1][5 - 1] + self.ans[10 - 1][j - 1][4 - 1] + \
                            self.ans[10 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                                6 - 1] + \
                            self.ans[3 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                                1 - 1]
                    self.model.addCons(sum49 <= 1)

                    sum50 = self.ans[5 - 1][j - 1][1 - 1] + self.ans[10 - 1][j - 1][4 - 1] + \
                            self.ans[10 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                                6 - 1] + \
                            self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                                3 - 1]
                    self.model.addCons(sum50 <= 1)

                    sum54 = self.ans[1 - 1][j - 1][3 - 1] + self.ans[10 - 1][j - 1][3 - 1] + \
                            self.ans[10 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                                1 - 1] + \
                            self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                                1 - 1]
                    self.model.addCons(sum54 <= 1)

                    sum57 = self.ans[2 - 1][j - 1][3 - 1] + self.ans[10 - 1][j - 1][3 - 1] + \
                            self.ans[10 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                                1 - 1] + \
                            self.ans[2 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                                1 - 1]
                    self.model.addCons(sum57 <= 1)

                    sum59 = self.ans[3 - 1][j - 1][4 - 1] + self.ans[10 - 1][j - 1][3 - 1] + \
                            self.ans[10 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                                1 - 1] + \
                            self.ans[3 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                                2 - 1]
                    self.model.addCons(sum59 <= 1)

                    sum60 = self.ans[5 - 1][j - 1][6 - 1] + self.ans[10 - 1][j - 1][3 - 1] + \
                            self.ans[10 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                                1 - 1] + \
                            self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                                4 - 1]
                    self.model.addCons(sum60 <= 1)

        elif designated_color == 'С':
            print("ОБОЗНАЧЕННЫЙ ЦВЕТ СИНИЙ")
            for j in range(1, self.n + 1):
                sum1 = self.ans[3 - 1][j - 1][3 - 1] + self.ans[5 - 1][j - 1][6 - 1] + \
                       self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][2 - 1] + \
                       self.ans[3 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][5 - 1]
                self.model.addCons(sum1 <= 1)

                sum7 = self.ans[3 - 1][j - 1][2 - 1] + self.ans[5 - 1][j - 1][5 - 1] + \
                       self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][3 - 1] + \
                       self.ans[3 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][6 - 1]
                self.model.addCons(sum7 <= 1)

                sum13 = self.ans[3 - 1][j - 1][1 - 1] + self.ans[5 - 1][j - 1][4 - 1] + \
                        self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][2 - 1] + \
                        self.ans[3 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][5 - 1]
                self.model.addCons(sum13 <= 1)

                sum19 = self.ans[3 - 1][j - 1][2 - 1] + self.ans[5 - 1][j - 1][5 - 1] + \
                        self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][1 - 1] + \
                        self.ans[3 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][4 - 1]
                self.model.addCons(sum19 <= 1)

                sum25 = self.ans[3 - 1][j - 1][1 - 1] + self.ans[5 - 1][j - 1][4 - 1] + \
                        self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][6 - 1] + \
                        self.ans[3 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][3 - 1]
                self.model.addCons(sum25 <= 1)

                sum31 = self.ans[3 - 1][j - 1][6 - 1] + self.ans[5 - 1][j - 1][3 - 1] + \
                        self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][1 - 1] + \
                        self.ans[3 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][4 - 1]
                self.model.addCons(sum31 <= 1)

                if len(self.ans) >= 6:  # т.к. в ограничениях есть фишка вида 6 (а фишек может быть всего 5)
                    sum2 = self.ans[3 - 1][j - 1][3 - 1] + self.ans[6 - 1][j - 1][6 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               2 - 1] + \
                           self.ans[3 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][5 - 1]
                    self.model.addCons(sum2 <= 1)

                    sum4 = self.ans[5 - 1][j - 1][6 - 1] + self.ans[6 - 1][j - 1][6 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               2 - 1] + \
                           self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][2 - 1]
                    self.model.addCons(sum4 <= 1)

                    sum8 = self.ans[3 - 1][j - 1][2 - 1] + self.ans[6 - 1][j - 1][5 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[3 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][6 - 1]
                    self.model.addCons(sum8 <= 1)

                    sum10 = self.ans[5 - 1][j - 1][5 - 1] + self.ans[6 - 1][j - 1][5 - 1] + \
                            self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                                3 - 1] + \
                            self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                                3 - 1]
                    self.model.addCons(sum10 <= 1)

                    sum14 = self.ans[3 - 1][j - 1][1 - 1] + self.ans[6 - 1][j - 1][4 - 1] + \
                            self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                                2 - 1] + \
                            self.ans[3 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                                5 - 1]
                    self.model.addCons(sum14 <= 1)

                    sum16 = self.ans[5 - 1][j - 1][4 - 1] + self.ans[6 - 1][j - 1][4 - 1] + \
                            self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                                2 - 1] + \
                            self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                                2 - 1]
                    self.model.addCons(sum16 <= 1)

                    sum20 = self.ans[3 - 1][j - 1][2 - 1] + self.ans[6 - 1][j - 1][5 - 1] + \
                            self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                                1 - 1] + \
                            self.ans[3 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                                4 - 1]
                    self.model.addCons(sum20 <= 1)

                    sum22 = self.ans[5 - 1][j - 1][5 - 1] + self.ans[6 - 1][j - 1][5 - 1] + \
                            self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                                1 - 1] + \
                            self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                                1 - 1]
                    self.model.addCons(sum22 <= 1)

                    sum26 = self.ans[3 - 1][j - 1][1 - 1] + self.ans[6 - 1][j - 1][4 - 1] + \
                            self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                                6 - 1] + \
                            self.ans[3 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                                3 - 1]
                    self.model.addCons(sum26 <= 1)

                    sum28 = self.ans[5 - 1][j - 1][4 - 1] + self.ans[6 - 1][j - 1][4 - 1] + \
                            self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                                6 - 1] + \
                            self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                                6 - 1]
                    self.model.addCons(sum28 <= 1)

                    sum32 = self.ans[3 - 1][j - 1][6 - 1] + self.ans[6 - 1][j - 1][3 - 1] + \
                            self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                                1 - 1] + \
                            self.ans[3 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                                4 - 1]
                    self.model.addCons(sum32 <= 1)

                    sum34 = self.ans[5 - 1][j - 1][3 - 1] + self.ans[6 - 1][j - 1][3 - 1] + \
                            self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                                1 - 1] + \
                            self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                                1 - 1]
                    self.model.addCons(sum34 <= 1)

                if len(self.ans) >= 7:  # т.к. в ограничениях есть фишка вида 7 (а фишек может быть всего 6)
                    sum3 = self.ans[3 - 1][j - 1][3 - 1] + self.ans[7 - 1][j - 1][6 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               2 - 1] + \
                           self.ans[3 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][5 - 1]
                    self.model.addCons(sum3 <= 1)

                    sum5 = self.ans[5 - 1][j - 1][6 - 1] + self.ans[7 - 1][j - 1][6 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               2 - 1] + \
                           self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][2 - 1]
                    self.model.addCons(sum5 <= 1)

                    sum6 = self.ans[6 - 1][j - 1][6 - 1] + self.ans[7 - 1][j - 1][6 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               2 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][2 - 1]
                    self.model.addCons(sum6 <= 1)

                    sum9 = self.ans[3 - 1][j - 1][2 - 1] + self.ans[7 - 1][j - 1][5 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[3 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][6 - 1]
                    self.model.addCons(sum9 <= 1)

                    sum11 = self.ans[5 - 1][j - 1][5 - 1] + self.ans[7 - 1][j - 1][5 - 1] + \
                            self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                                3 - 1] + \
                            self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                                3 - 1]
                    self.model.addCons(sum11 <= 1)

                    sum12 = self.ans[6 - 1][j - 1][5 - 1] + self.ans[7 - 1][j - 1][5 - 1] + \
                            self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                                3 - 1] + \
                            self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                                3 - 1]
                    self.model.addCons(sum12 <= 1)

                    sum15 = self.ans[3 - 1][j - 1][1 - 1] + self.ans[7 - 1][j - 1][4 - 1] + \
                            self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                                2 - 1] + \
                            self.ans[3 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                                5 - 1]
                    self.model.addCons(sum15 <= 1)

                    sum17 = self.ans[5 - 1][j - 1][4 - 1] + self.ans[7 - 1][j - 1][4 - 1] + \
                            self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                                2 - 1] + \
                            self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                                2 - 1]
                    self.model.addCons(sum17 <= 1)

                    sum18 = self.ans[6 - 1][j - 1][4 - 1] + self.ans[7 - 1][j - 1][4 - 1] + \
                            self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                                2 - 1] + \
                            self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                                2 - 1]
                    self.model.addCons(sum18 <= 1)

                    sum21 = self.ans[3 - 1][j - 1][2 - 1] + self.ans[7 - 1][j - 1][5 - 1] + \
                            self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                                1 - 1] + \
                            self.ans[3 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                                4 - 1]
                    self.model.addCons(sum21 <= 1)

                    sum23 = self.ans[5 - 1][j - 1][5 - 1] + self.ans[7 - 1][j - 1][5 - 1] + \
                            self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                                1 - 1] + \
                            self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                                1 - 1]
                    self.model.addCons(sum23 <= 1)

                    sum24 = self.ans[6 - 1][j - 1][5 - 1] + self.ans[7 - 1][j - 1][5 - 1] + \
                            self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                                1 - 1] + \
                            self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                                1 - 1]
                    self.model.addCons(sum24 <= 1)

                    sum27 = self.ans[3 - 1][j - 1][1 - 1] + self.ans[7 - 1][j - 1][4 - 1] + \
                            self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                                6 - 1] + \
                            self.ans[3 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                                3 - 1]
                    self.model.addCons(sum27 <= 1)

                    sum29 = self.ans[5 - 1][j - 1][4 - 1] + self.ans[7 - 1][j - 1][4 - 1] + \
                            self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                                6 - 1] + \
                            self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                                6 - 1]
                    self.model.addCons(sum29 <= 1)

                    sum30 = self.ans[6 - 1][j - 1][4 - 1] + self.ans[7 - 1][j - 1][4 - 1] + \
                            self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                                6 - 1] + \
                            self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                                6 - 1]
                    self.model.addCons(sum30 <= 1)

                    sum33 = self.ans[3 - 1][j - 1][6 - 1] + self.ans[7 - 1][j - 1][3 - 1] + \
                            self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                                1 - 1] + \
                            self.ans[3 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                                4 - 1]
                    self.model.addCons(sum33 <= 1)

                    sum35 = self.ans[5 - 1][j - 1][3 - 1] + self.ans[7 - 1][j - 1][3 - 1] + \
                            self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                                1 - 1] + \
                            self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                                1 - 1]
                    self.model.addCons(sum35 <= 1)

                    sum36 = self.ans[6 - 1][j - 1][3 - 1] + self.ans[7 - 1][j - 1][3 - 1] + \
                            self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                                1 - 1] + \
                            self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                                1 - 1]
                    self.model.addCons(sum36 <= 1)

    # Оптимизация (Ограничения С7-С9) - убираем подциклы из 3, 4, 5 фишек при n>5
    def cons_8(self, is_spiral, chosen_field, sub_functions):
        """
            Убираем подциклы из 4 фишек для обозначенного цвета (т.е. убираем конкретные расположения конкретных фишек)
        """
        designated_color = sub_functions.get_designated_color(self.n_new)  # получение обозн. цвета (буква К, Ж или С)
        # print(f'designated_color={designated_color}')
        # если обозначенный цвет красный (К)
        if designated_color == 'К':
            print("ОБОЗНАЧЕННЫЙ ЦВЕТ КРАСНЫЙ")
            for j in range(1, self.n + 1):
                if len(self.ans) >= 10:
                    sum1 = self.ans[1 - 1][j - 1][2 - 1] + self.ans[4 - 1][j - 1][1 - 1] + self.ans[6 - 1][j - 1][
                        4 - 1] + self.ans[7 - 1][j - 1][2 - 1] + self.ans[8 - 1][j - 1][3 - 1] + \
                           self.ans[10 - 1][j - 1][3 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               1 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[10 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               6 - 1]
                    self.model.addCons(sum1 <= 1)

                    sum6 = self.ans[1 - 1][j - 1][1 - 1] + self.ans[4 - 1][j - 1][6 - 1] + self.ans[6 - 1][j - 1][
                        3 - 1] + self.ans[7 - 1][j - 1][1 - 1] + self.ans[8 - 1][j - 1][2 - 1] + \
                           self.ans[10 - 1][j - 1][2 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[10 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1]
                    self.model.addCons(sum6 <= 1)

                    sum11 = self.ans[1 - 1][j - 1][6 - 1] + self.ans[4 - 1][j - 1][5 - 1] + self.ans[6 - 1][j - 1][
                        2 - 1] + self.ans[7 - 1][j - 1][6 - 1] + self.ans[8 - 1][j - 1][1 - 1] + \
                            self.ans[10 - 1][j - 1][1 - 1] + \
                            self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                                3 - 1] + \
                            self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                                2 - 1] + \
                            self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                                5 - 1] + \
                            self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                                3 - 1] + \
                            self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                                4 - 1] + \
                            self.ans[10 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                                4 - 1]
                    self.model.addCons(sum11 <= 1)

                elif len(self.ans) >= 8:
                    sum2 = self.ans[1 - 1][j - 1][2 - 1] + self.ans[4 - 1][j - 1][1 - 1] + self.ans[6 - 1][j - 1][
                        4 - 1] + self.ans[7 - 1][j - 1][2 - 1] + self.ans[8 - 1][j - 1][3 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               1 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               6 - 1]
                    self.model.addCons(sum2 <= 1)

                    sum7 = self.ans[1 - 1][j - 1][1 - 1] + self.ans[4 - 1][j - 1][6 - 1] + self.ans[6 - 1][j - 1][
                        3 - 1] + self.ans[7 - 1][j - 1][1 - 1] + self.ans[8 - 1][j - 1][2 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1]
                    self.model.addCons(sum7 <= 1)

                    sum12 = self.ans[1 - 1][j - 1][6 - 1] + self.ans[4 - 1][j - 1][5 - 1] + self.ans[6 - 1][j - 1][
                        2 - 1] + self.ans[7 - 1][j - 1][6 - 1] + self.ans[8 - 1][j - 1][1 - 1] + \
                            self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                                3 - 1] + \
                            self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                                2 - 1] + \
                            self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                                5 - 1] + \
                            self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                                3 - 1] + \
                            self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                                4 - 1]
                    self.model.addCons(sum12 <= 1)

                elif len(self.ans) >= 7:
                    sum3 = self.ans[1 - 1][j - 1][2 - 1] + self.ans[4 - 1][j - 1][1 - 1] + self.ans[6 - 1][j - 1][
                        4 - 1] + self.ans[7 - 1][j - 1][2 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               1 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               5 - 1]
                    self.model.addCons(sum3 <= 1)

                    sum8 = self.ans[1 - 1][j - 1][1 - 1] + self.ans[4 - 1][j - 1][6 - 1] + self.ans[6 - 1][j - 1][
                        3 - 1] + self.ans[7 - 1][j - 1][1 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1]
                    self.model.addCons(sum8 <= 1)

                    sum13 = self.ans[1 - 1][j - 1][6 - 1] + self.ans[4 - 1][j - 1][5 - 1] + self.ans[6 - 1][j - 1][
                        2 - 1] + self.ans[7 - 1][j - 1][6 - 1] + \
                            self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                                3 - 1] + \
                            self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                                2 - 1] + \
                            self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                                5 - 1] + \
                            self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                                3 - 1]
                    self.model.addCons(sum13 <= 1)

                elif len(self.ans) >= 6:
                    sum4 = self.ans[1 - 1][j - 1][2 - 1] + self.ans[4 - 1][j - 1][1 - 1] + self.ans[6 - 1][j - 1][
                        4 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               1 - 1]
                    self.model.addCons(sum4 <= 1)

                    sum9 = self.ans[1 - 1][j - 1][1 - 1] + self.ans[4 - 1][j - 1][6 - 1] + self.ans[6 - 1][j - 1][
                        3 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               6 - 1]
                    self.model.addCons(sum9 <= 1)

                    sum14 = self.ans[1 - 1][j - 1][6 - 1] + self.ans[4 - 1][j - 1][5 - 1] + self.ans[6 - 1][j - 1][
                        2 - 1] + \
                            self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                                3 - 1] + \
                            self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                                2 - 1] + \
                            self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                                5 - 1]
                    self.model.addCons(sum14 <= 1)

                else:
                    sum5 = self.ans[1 - 1][j - 1][2 - 1] + self.ans[4 - 1][j - 1][1 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               4 - 1]
                    self.model.addCons(sum5 <= 1)

                    sum10 = self.ans[1 - 1][j - 1][1 - 1] + self.ans[4 - 1][j - 1][6 - 1] + \
                            self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                                4 - 1] + \
                            self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                                3 - 1]
                    self.model.addCons(sum10 <= 1)

                    sum15 = self.ans[1 - 1][j - 1][6 - 1] + self.ans[4 - 1][j - 1][5 - 1] + \
                            self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                                3 - 1] + \
                            self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                                2 - 1]
                    self.model.addCons(sum15 <= 1)

        # если обозначенный цвет синий (С)
        if designated_color == 'С':
            print("ОБОЗНАЧЕННЫЙ ЦВЕТ СИНИЙ")
            for j in range(1, self.n + 1):
                if len(self.ans) >= 10:
                    sum1 = self.ans[1 - 1][j - 1][3 - 1] + self.ans[8 - 1][j - 1][1 - 1] + self.ans[9 - 1][j - 1][
                        1 - 1] + \
                           self.ans[10 - 1][j - 1][2 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[9 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[10 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               5 - 1]
                    self.model.addCons(sum1 <= 1)

                    sum5 = self.ans[1 - 1][j - 1][2 - 1] + self.ans[8 - 1][j - 1][6 - 1] + self.ans[9 - 1][j - 1][
                        6 - 1] + \
                           self.ans[10 - 1][j - 1][1 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[9 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[10 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1]
                    self.model.addCons(sum5 <= 1)

                    sum9 = self.ans[1 - 1][j - 1][1 - 1] + self.ans[8 - 1][j - 1][5 - 1] + self.ans[9 - 1][j - 1][
                        5 - 1] + \
                           self.ans[10 - 1][j - 1][6 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               2 - 1] + \
                           self.ans[9 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               2 - 1] + \
                           self.ans[10 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               3 - 1]
                    self.model.addCons(sum9 <= 1)


                elif len(self.ans) >= 9:
                    sum2 = self.ans[1 - 1][j - 1][3 - 1] + self.ans[8 - 1][j - 1][1 - 1] + self.ans[9 - 1][j - 1][
                        1 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[9 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][4 - 1]
                    self.model.addCons(sum2 <= 1)

                    sum6 = self.ans[1 - 1][j - 1][2 - 1] + self.ans[8 - 1][j - 1][6 - 1] + self.ans[9 - 1][j - 1][
                        6 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[9 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               3 - 1]
                    self.model.addCons(sum6 <= 1)

                    sum10 = self.ans[1 - 1][j - 1][1 - 1] + self.ans[8 - 1][j - 1][5 - 1] + self.ans[9 - 1][j - 1][
                        5 - 1] + \
                            self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                                4 - 1] + \
                            self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                                2 - 1] + \
                            self.ans[9 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                                2 - 1]
                    self.model.addCons(sum10 <= 1)

                elif len(self.ans) >= 8:
                    sum3 = self.ans[1 - 1][j - 1][3 - 1] + self.ans[8 - 1][j - 1][1 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               4 - 1]
                    self.model.addCons(sum3 <= 1)

                    sum7 = self.ans[1 - 1][j - 1][2 - 1] + self.ans[8 - 1][j - 1][6 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               3 - 1]
                    self.model.addCons(sum7 <= 1)

                    sum11 = self.ans[1 - 1][j - 1][1 - 1] + self.ans[8 - 1][j - 1][5 - 1] + \
                            self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                                4 - 1] + \
                            self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                                2 - 1]
                    self.model.addCons(sum11 <= 1)

                else:
                    sum4 = self.ans[1 - 1][j - 1][3 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               6 - 1]
                    self.model.addCons(sum4 <= 1)

                    sum8 = self.ans[1 - 1][j - 1][2 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1]
                    self.model.addCons(sum8 <= 1)

                    sum12 = self.ans[1 - 1][j - 1][1 - 1] + \
                            self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                                4 - 1]
                    self.model.addCons(sum12 <= 1)

        if designated_color == 'Ж':
            print("ОБОЗНАЧЕННЫЙ ЦВЕТ ЖЕЛТЫЙ")
            for j in range(1, self.n + 1):
                if len(self.ans) >= 9:
                    sum1 = self.ans[4 - 1][j - 1][4 - 1] + self.ans[6 - 1][j - 1][3 - 1] + self.ans[7 - 1][j - 1][
                        2 - 1] + \
                           self.ans[9 - 1][j - 1][4 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               1 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[9 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               1 - 1]
                    self.model.addCons(sum1 <= 1)

                    sum5 = self.ans[4 - 1][j - 1][3 - 1] + self.ans[6 - 1][j - 1][2 - 1] + self.ans[7 - 1][j - 1][
                        1 - 1] + \
                           self.ans[9 - 1][j - 1][3 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[9 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               6 - 1]
                    self.model.addCons(sum5 <= 1)

                    sum9 = self.ans[4 - 1][j - 1][2 - 1] + self.ans[6 - 1][j - 1][1 - 1] + self.ans[7 - 1][j - 1][
                        6 - 1] + \
                           self.ans[9 - 1][j - 1][2 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[9 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               5 - 1]
                    self.model.addCons(sum9 <= 1)

                elif len(self.ans) >= 7:
                    sum2 = self.ans[4 - 1][j - 1][4 - 1] + self.ans[6 - 1][j - 1][3 - 1] + self.ans[7 - 1][j - 1][
                        2 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               1 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               5 - 1]
                    self.model.addCons(sum2 <= 1)

                    sum6 = self.ans[4 - 1][j - 1][3 - 1] + self.ans[6 - 1][j - 1][2 - 1] + self.ans[7 - 1][j - 1][
                        1 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1]
                    self.model.addCons(sum6 <= 1)

                    sum10 = self.ans[4 - 1][j - 1][2 - 1] + self.ans[6 - 1][j - 1][1 - 1] + self.ans[7 - 1][j - 1][
                        6 - 1] + \
                            self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                                5 - 1] + \
                            self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                                4 - 1] + \
                            self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                                3 - 1]
                    self.model.addCons(sum10 <= 1)

                elif len(self.ans) >= 6:
                    sum3 = self.ans[4 - 1][j - 1][4 - 1] + self.ans[6 - 1][j - 1][3 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               1 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               6 - 1]
                    self.model.addCons(sum3 <= 1)

                    sum7 = self.ans[4 - 1][j - 1][3 - 1] + self.ans[6 - 1][j - 1][2 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1]
                    self.model.addCons(sum7 <= 1)

                    sum11 = self.ans[4 - 1][j - 1][2 - 1] + self.ans[6 - 1][j - 1][1 - 1] + \
                            self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                                5 - 1] + \
                            self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                                4 - 1]
                    self.model.addCons(sum11 <= 1)

                else:
                    sum4 = self.ans[4 - 1][j - 1][4 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               1 - 1]
                    self.model.addCons(sum4 <= 1)

                    sum8 = self.ans[4 - 1][j - 1][3 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               6 - 1]
                    self.model.addCons(sum8 <= 1)

                    sum12 = self.ans[4 - 1][j - 1][2 - 1] + \
                            self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                                5 - 1]
                    self.model.addCons(sum12 <= 1)

    # Оптимизация (Ограничения С7-С9) - убираем подциклы из 3, 4, 5 фишек при n>5
    def cons_9(self, is_spiral, chosen_field, sub_functions):
        """
            Убираем подциклы из 5 фишек для обозначенного цвета (т.е. убираем конкретные расположения конкретных фишек)
        """
        designated_color = sub_functions.get_designated_color(self.n_new)  # получение обозн. цвета (буква К, Ж или С)
        if designated_color == 'К':
            print("ОБОЗНАЧЕННЫЙ ЦВЕТ КРАСНЫЙ")
            for j in range(1, self.n + 1):
                if len(self.ans) >= 10:
                    sum1 = self.ans[5 - 1][j - 1][2 - 1] + self.ans[5 - 1][j - 1][5 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               1 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1] + self.ans[9 - 1][j - 1][2 - 1] + self.ans[9 - 1][j - 1][5 - 1] + \
                           self.ans[10 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[10 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1]

                    self.model.addCons(sum1 <= 2)

                    sum2 = self.ans[1 - 1][j - 1][1 - 1] + self.ans[4 - 1][j - 1][6 - 1] + \
                           self.ans[7 - 1][j - 1][1 - 1] + \
                           self.ans[8 - 1][j - 1][2 - 1] + \
                           self.ans[10 - 1][j - 1][2 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               2 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               1 - 1] + \
                           self.ans[10 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               1 - 1] + \
                           self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               1 - 1] + \
                           self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[9 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               1 - 1] + \
                           self.ans[9 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1]

                    self.model.addCons(sum2 <= 2)

                    sum3 = self.ans[1 - 1][j - 1][2 - 1] + self.ans[4 - 1][j - 1][1 - 1] + \
                           self.ans[6 - 1][j - 1][4 - 1] + \
                           self.ans[7 - 1][j - 1][2 - 1] + \
                           self.ans[8 - 1][j - 1][3 - 1] + \
                           self.ans[10 - 1][j - 1][3 - 1] + \
                           self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[9 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[9 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[10 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1]

                    self.model.addCons(sum3 <= 2)

                    sum4 = self.ans[5 - 1][j - 1][1 - 1] + self.ans[5 - 1][j - 1][4 - 1] + \
                           self.ans[9 - 1][j - 1][1 - 1] + \
                           self.ans[9 - 1][j - 1][4 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[10 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               2 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[10 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               4 - 1]

                    self.model.addCons(sum4 <= 2)

                    sum5 = self.ans[1 - 1][j - 1][6 - 1] + self.ans[4 - 1][j - 1][5 - 1] + \
                           self.ans[6 - 1][j - 1][2 - 1] + \
                           self.ans[7 - 1][j - 1][6 - 1] + \
                           self.ans[8 - 1][j - 1][1 - 1] + \
                           self.ans[10 - 1][j - 1][1 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               1 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[10 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[9 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[9 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               6 - 1]

                    self.model.addCons(sum5 <= 2)

                    sum6 = self.ans[1 - 1][j - 1][1 - 1] + self.ans[4 - 1][j - 1][6 - 1] + \
                           self.ans[6 - 1][j - 1][3 - 1] + \
                           self.ans[7 - 1][j - 1][1 - 1] + \
                           self.ans[8 - 1][j - 1][2 - 1] + \
                           self.ans[10 - 1][j - 1][2 - 1] + \
                           self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               2 - 1] + \
                           self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[9 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               2 - 1] + \
                           self.ans[9 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               2 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               1 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               2 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[10 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               3 - 1]

                    self.model.addCons(sum6 <= 2)

                elif len(self.ans) >= 9:
                    sum1 = self.ans[5 - 1][j - 1][2 - 1] + self.ans[5 - 1][j - 1][5 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               1 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1] + self.ans[9 - 1][j - 1][2 - 1] + self.ans[9 - 1][j - 1][5 - 1]

                    self.model.addCons(sum1 <= 2)

                    sum2 = self.ans[1 - 1][j - 1][1 - 1] + self.ans[4 - 1][j - 1][6 - 1] + \
                           self.ans[7 - 1][j - 1][1 - 1] + \
                           self.ans[8 - 1][j - 1][2 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               2 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               1 - 1] + \
                           self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               1 - 1] + \
                           self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[9 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               1 - 1] + \
                           self.ans[9 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1]

                    self.model.addCons(sum2 <= 2)

                    sum3 = self.ans[1 - 1][j - 1][2 - 1] + self.ans[4 - 1][j - 1][1 - 1] + \
                           self.ans[6 - 1][j - 1][4 - 1] + \
                           self.ans[7 - 1][j - 1][2 - 1] + \
                           self.ans[8 - 1][j - 1][3 - 1] + \
                           self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[9 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[9 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1]

                    self.model.addCons(sum3 <= 2)

                    sum4 = self.ans[5 - 1][j - 1][1 - 1] + self.ans[5 - 1][j - 1][4 - 1] + \
                           self.ans[9 - 1][j - 1][1 - 1] + \
                           self.ans[9 - 1][j - 1][4 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               2 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               4 - 1]

                    self.model.addCons(sum4 <= 2)

                    sum5 = self.ans[1 - 1][j - 1][6 - 1] + self.ans[4 - 1][j - 1][5 - 1] + \
                           self.ans[6 - 1][j - 1][2 - 1] + \
                           self.ans[7 - 1][j - 1][6 - 1] + \
                           self.ans[8 - 1][j - 1][1 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               1 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[9 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[9 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               6 - 1]

                    self.model.addCons(sum5 <= 2)

                    sum6 = self.ans[1 - 1][j - 1][1 - 1] + self.ans[4 - 1][j - 1][6 - 1] + \
                           self.ans[6 - 1][j - 1][3 - 1] + \
                           self.ans[7 - 1][j - 1][1 - 1] + \
                           self.ans[8 - 1][j - 1][2 - 1] + \
                           self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               2 - 1] + \
                           self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[9 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               2 - 1] + \
                           self.ans[9 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               2 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               1 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               2 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               3 - 1]

                    self.model.addCons(sum6 <= 2)

                elif len(self.ans) >= 8:
                    sum1 = self.ans[5 - 1][j - 1][2 - 1] + self.ans[5 - 1][j - 1][5 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               1 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1]

                    self.model.addCons(sum1 <= 2)

                    sum2 = self.ans[1 - 1][j - 1][1 - 1] + self.ans[4 - 1][j - 1][6 - 1] + \
                           self.ans[7 - 1][j - 1][1 - 1] + \
                           self.ans[8 - 1][j - 1][2 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               2 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               1 - 1] + \
                           self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               1 - 1] + \
                           self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1]

                    self.model.addCons(sum2 <= 2)

                    sum3 = self.ans[1 - 1][j - 1][2 - 1] + self.ans[4 - 1][j - 1][1 - 1] + \
                           self.ans[6 - 1][j - 1][4 - 1] + \
                           self.ans[7 - 1][j - 1][2 - 1] + \
                           self.ans[8 - 1][j - 1][3 - 1] + \
                           self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1]

                    self.model.addCons(sum3 <= 2)

                    sum4 = self.ans[5 - 1][j - 1][1 - 1] + self.ans[5 - 1][j - 1][4 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               2 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               4 - 1]

                    self.model.addCons(sum4 <= 2)

                    sum5 = self.ans[1 - 1][j - 1][6 - 1] + self.ans[4 - 1][j - 1][5 - 1] + \
                           self.ans[6 - 1][j - 1][2 - 1] + \
                           self.ans[7 - 1][j - 1][6 - 1] + \
                           self.ans[8 - 1][j - 1][1 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               1 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               6 - 1]

                    self.model.addCons(sum5 <= 2)

                    sum6 = self.ans[1 - 1][j - 1][1 - 1] + self.ans[4 - 1][j - 1][6 - 1] + \
                           self.ans[6 - 1][j - 1][3 - 1] + \
                           self.ans[7 - 1][j - 1][1 - 1] + \
                           self.ans[8 - 1][j - 1][2 - 1] + \
                           self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               2 - 1] + \
                           self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               2 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               1 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               2 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               3 - 1]

                    self.model.addCons(sum6 <= 2)

                elif len(self.ans) >= 7:
                    sum1 = self.ans[5 - 1][j - 1][2 - 1] + self.ans[5 - 1][j - 1][5 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               1 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1]

                    self.model.addCons(sum1 <= 2)

                    sum2 = self.ans[1 - 1][j - 1][1 - 1] + self.ans[4 - 1][j - 1][6 - 1] + \
                           self.ans[7 - 1][j - 1][1 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               2 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               1 - 1] + \
                           self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1]

                    self.model.addCons(sum2 <= 2)

                    sum3 = self.ans[1 - 1][j - 1][2 - 1] + self.ans[4 - 1][j - 1][1 - 1] + \
                           self.ans[6 - 1][j - 1][4 - 1] + \
                           self.ans[7 - 1][j - 1][2 - 1] + \
                           self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1]

                    self.model.addCons(sum3 <= 2)

                    sum4 = self.ans[5 - 1][j - 1][1 - 1] + self.ans[5 - 1][j - 1][4 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               2 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               3 - 1]

                    self.model.addCons(sum4 <= 2)

                    sum5 = self.ans[1 - 1][j - 1][6 - 1] + self.ans[4 - 1][j - 1][5 - 1] + \
                           self.ans[6 - 1][j - 1][2 - 1] + \
                           self.ans[7 - 1][j - 1][6 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               1 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               6 - 1]

                    self.model.addCons(sum5 <= 2)

                    sum6 = self.ans[1 - 1][j - 1][1 - 1] + self.ans[4 - 1][j - 1][6 - 1] + \
                           self.ans[6 - 1][j - 1][3 - 1] + \
                           self.ans[7 - 1][j - 1][1 - 1] + \
                           self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               2 - 1] + \
                           self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               2 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               1 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               2 - 1]

                    self.model.addCons(sum6 <= 2)

                elif len(self.ans) >= 6:    # Ограничения С7-С9 касаются задач с кол-вом фишек > 5.
                    sum1 = self.ans[5 - 1][j - 1][2 - 1] + self.ans[5 - 1][j - 1][5 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               1 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               6 - 1]

                    self.model.addCons(sum1 <= 2)

                    sum2 = self.ans[1 - 1][j - 1][1 - 1] + self.ans[4 - 1][j - 1][6 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               2 - 1] + \
                           self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               1 - 1] + \
                           self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1]

                    self.model.addCons(sum2 <= 2)

                    sum3 = self.ans[1 - 1][j - 1][2 - 1] + self.ans[4 - 1][j - 1][1 - 1] + \
                           self.ans[6 - 1][j - 1][4 - 1] + \
                           self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               6 - 1]

                    self.model.addCons(sum3 <= 2)

                    sum4 = self.ans[5 - 1][j - 1][1 - 1] + self.ans[5 - 1][j - 1][4 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               2 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               5 - 1]

                    self.model.addCons(sum4 <= 2)

                    sum5 = self.ans[1 - 1][j - 1][6 - 1] + self.ans[4 - 1][j - 1][5 - 1] + \
                           self.ans[6 - 1][j - 1][2 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               1 - 1] + \
                           self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               6 - 1]

                    self.model.addCons(sum5 <= 2)

                    sum6 = self.ans[1 - 1][j - 1][1 - 1] + self.ans[4 - 1][j - 1][6 - 1] + \
                           self.ans[6 - 1][j - 1][3 - 1] + \
                           self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               2 - 1] + \
                           self.ans[5 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               2 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               1 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               4 - 1]

                    self.model.addCons(sum6 <= 2)

        if designated_color == 'С':
            print("ОБОЗНАЧЕННЫЙ ЦВЕТ СИНИЙ")
            for j in range(1, self.n + 1):
                if len(self.ans) >= 10:
                    sum1 = self.ans[1 - 1][j - 1][2 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               1 - 1] + \
                           self.ans[2 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               1 - 1] + \
                           self.ans[2 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               1 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[8 - 1][j - 1][6 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[9 - 1][j - 1][6 - 1] + \
                           self.ans[9 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[10 - 1][j - 1][1 - 1] + \
                           self.ans[10 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               2 - 1]

                    self.model.addCons(sum1 <= 2)

                    sum2 = self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[2 - 1][j - 1][1 - 1] + \
                           self.ans[2 - 1][j - 1][4 - 1] + \
                           self.ans[4 - 1][j - 1][1 - 1] + \
                           self.ans[4 - 1][j - 1][4 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               2 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[9 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               2 - 1] + \
                           self.ans[9 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[10 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[10 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1]

                    self.model.addCons(sum2 <= 2)

                    sum3 = self.ans[2 - 1][j - 1][2 - 1] + \
                           self.ans[2 - 1][j - 1][5 - 1] + \
                           self.ans[4 - 1][j - 1][2 - 1] + \
                           self.ans[4 - 1][j - 1][5 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[9 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[9 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[10 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[10 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               5 - 1]

                    self.model.addCons(sum3 <= 2)

                    sum4 = self.ans[1 - 1][j - 1][2 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[2 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               2 - 1] + \
                           self.ans[2 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               2 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[8 - 1][j - 1][2 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               1 - 1] + \
                           self.ans[9 - 1][j - 1][2 - 1] + \
                           self.ans[9 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               1 - 1] + \
                           self.ans[10 - 1][j - 1][1 - 1] + \
                           self.ans[10 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               2 - 1]

                    self.model.addCons(sum4 <= 2)

                    sum5 = self.ans[1 - 1][j - 1][3 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[2 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[2 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[8 - 1][j - 1][1 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               2 - 1] + \
                           self.ans[9 - 1][j - 1][1 - 1] + \
                           self.ans[9 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               2 - 1] + \
                           self.ans[10 - 1][j - 1][2 - 1] + \
                           self.ans[10 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               3 - 1]

                    self.model.addCons(sum5 <= 2)

                    sum6 = self.ans[1 - 1][j - 1][1 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[2 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[2 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[8 - 1][j - 1][5 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[9 - 1][j - 1][5 - 1] + \
                           self.ans[9 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[10 - 1][j - 1][6 - 1] + \
                           self.ans[10 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1]

                    self.model.addCons(sum6 <= 2)

                elif len(self.ans) >= 9:
                    sum1 = self.ans[1 - 1][j - 1][2 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               1 - 1] + \
                           self.ans[2 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               1 - 1] + \
                           self.ans[2 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               1 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[8 - 1][j - 1][6 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[9 - 1][j - 1][6 - 1] + \
                           self.ans[9 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               5 - 1]

                    self.model.addCons(sum1 <= 2)

                    sum2 = self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[2 - 1][j - 1][1 - 1] + \
                           self.ans[2 - 1][j - 1][4 - 1] + \
                           self.ans[4 - 1][j - 1][1 - 1] + \
                           self.ans[4 - 1][j - 1][4 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               2 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[9 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               2 - 1] + \
                           self.ans[9 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               3 - 1]

                    self.model.addCons(sum2 <= 2)

                    sum3 = self.ans[2 - 1][j - 1][2 - 1] + \
                           self.ans[2 - 1][j - 1][5 - 1] + \
                           self.ans[4 - 1][j - 1][2 - 1] + \
                           self.ans[4 - 1][j - 1][5 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[9 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[9 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               4 - 1]

                    self.model.addCons(sum3 <= 2)

                    sum4 = self.ans[1 - 1][j - 1][2 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[2 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               2 - 1] + \
                           self.ans[2 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               2 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[8 - 1][j - 1][2 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               1 - 1] + \
                           self.ans[9 - 1][j - 1][2 - 1] + \
                           self.ans[9 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               1 - 1]

                    self.model.addCons(sum4 <= 2)

                    sum5 = self.ans[1 - 1][j - 1][3 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[2 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[2 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[8 - 1][j - 1][1 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               2 - 1] + \
                           self.ans[9 - 1][j - 1][1 - 1] + \
                           self.ans[9 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               2 - 1]

                    self.model.addCons(sum5 <= 2)

                    sum6 = self.ans[1 - 1][j - 1][1 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[2 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[2 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[8 - 1][j - 1][5 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[9 - 1][j - 1][5 - 1] + \
                           self.ans[9 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1]

                    self.model.addCons(sum6 <= 2)

                elif len(self.ans) >= 8:
                    sum1 = self.ans[1 - 1][j - 1][2 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               1 - 1] + \
                           self.ans[2 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               1 - 1] + \
                           self.ans[2 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               1 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[8 - 1][j - 1][6 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               5 - 1]

                    self.model.addCons(sum1 <= 2)

                    sum2 = self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[2 - 1][j - 1][1 - 1] + \
                           self.ans[2 - 1][j - 1][4 - 1] + \
                           self.ans[4 - 1][j - 1][1 - 1] + \
                           self.ans[4 - 1][j - 1][4 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               2 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               3 - 1]

                    self.model.addCons(sum2 <= 2)

                    sum3 = self.ans[2 - 1][j - 1][2 - 1] + \
                           self.ans[2 - 1][j - 1][5 - 1] + \
                           self.ans[4 - 1][j - 1][2 - 1] + \
                           self.ans[4 - 1][j - 1][5 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               4 - 1]

                    self.model.addCons(sum3 <= 2)

                    sum4 = self.ans[1 - 1][j - 1][2 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[2 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               2 - 1] + \
                           self.ans[2 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               2 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[8 - 1][j - 1][2 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               1 - 1]

                    self.model.addCons(sum4 <= 2)

                    sum5 = self.ans[1 - 1][j - 1][3 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[2 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[2 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[8 - 1][j - 1][1 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               2 - 1]

                    self.model.addCons(sum5 <= 2)

                    sum6 = self.ans[1 - 1][j - 1][1 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[2 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[2 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[8 - 1][j - 1][5 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1]

                    self.model.addCons(sum6 <= 2)

                else:   # для всех остальных случаев (здесь фигурируют фишки вида 1,2,4)
                    sum1 = self.ans[1 - 1][j - 1][2 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               1 - 1] + \
                           self.ans[2 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               1 - 1] + \
                           self.ans[2 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               1 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1]

                    self.model.addCons(sum1 <= 2)

                    sum2 = self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[2 - 1][j - 1][1 - 1] + \
                           self.ans[2 - 1][j - 1][4 - 1] + \
                           self.ans[4 - 1][j - 1][1 - 1] + \
                           self.ans[4 - 1][j - 1][4 - 1]

                    self.model.addCons(sum2 <= 2)

                    sum3 = self.ans[2 - 1][j - 1][2 - 1] + \
                           self.ans[2 - 1][j - 1][5 - 1] + \
                           self.ans[4 - 1][j - 1][2 - 1] + \
                           self.ans[4 - 1][j - 1][5 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               6 - 1]

                    self.model.addCons(sum3 <= 2)

                    sum4 = self.ans[1 - 1][j - 1][2 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[2 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               2 - 1] + \
                           self.ans[2 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               2 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1]

                    self.model.addCons(sum4 <= 2)

                    sum5 = self.ans[1 - 1][j - 1][3 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[2 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[2 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               6 - 1]

                    self.model.addCons(sum5 <= 2)

                    sum6 = self.ans[1 - 1][j - 1][1 - 1] + \
                           self.ans[1 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[2 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[2 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               6 - 1]

                    self.model.addCons(sum6 <= 2)

        if designated_color == 'Ж':
            print("ОБОЗНАЧЕННЫЙ ЦВЕТ ЖЕЛТЫЙ")
            for j in range(1, self.n + 1):
                if len(self.ans) >= 9:
                    sum1 = self.ans[4 - 1][j - 1][3 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               2 - 1] + \
                           self.ans[6 - 1][j - 1][2 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               1 - 1] + \
                           self.ans[7 - 1][j - 1][1 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               1 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[9 - 1][j - 1][3 - 1] + \
                           self.ans[9 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               2 - 1]

                    self.model.addCons(sum1 <= 2)

                    sum2 = self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[8 - 1][j - 1][1 - 1] + \
                           self.ans[8 - 1][j - 1][4 - 1] + \
                           self.ans[9 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[9 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               6 - 1]

                    self.model.addCons(sum2 <= 2)

                    sum3 = self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               1 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[8 - 1][j - 1][2 - 1] + \
                           self.ans[8 - 1][j - 1][5 - 1] + \
                           self.ans[9 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[9 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               1 - 1]

                    self.model.addCons(sum3 <= 2)

                    sum4 = self.ans[4 - 1][j - 1][4 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[6 - 1][j - 1][3 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[7 - 1][j - 1][2 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[9 - 1][j - 1][4 - 1] + \
                           self.ans[9 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1]

                    self.model.addCons(sum4 <= 2)

                    sum5 = self.ans[4 - 1][j - 1][3 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[6 - 1][j - 1][2 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[7 - 1][j - 1][1 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               2 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               2 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[9 - 1][j - 1][3 - 1] + \
                           self.ans[9 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               4 - 1]

                    self.model.addCons(sum5 <= 2)

                    sum6 = self.ans[4 - 1][j - 1][2 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               1 - 1] + \
                           self.ans[6 - 1][j - 1][1 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[7 - 1][j - 1][6 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[9 - 1][j - 1][2 - 1] + \
                           self.ans[9 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               1 - 1]

                    self.model.addCons(sum6 <= 2)

                elif len(self.ans) >= 8:
                    sum1 = self.ans[4 - 1][j - 1][3 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               2 - 1] + \
                           self.ans[6 - 1][j - 1][2 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               1 - 1] + \
                           self.ans[7 - 1][j - 1][1 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               1 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1]

                    self.model.addCons(sum1 <= 2)

                    sum2 = self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[8 - 1][j - 1][1 - 1] + \
                           self.ans[8 - 1][j - 1][4 - 1]

                    self.model.addCons(sum2 <= 2)

                    sum3 = self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               1 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[8 - 1][j - 1][2 - 1] + \
                           self.ans[8 - 1][j - 1][5 - 1]

                    self.model.addCons(sum3 <= 2)

                    sum4 = self.ans[4 - 1][j - 1][4 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[6 - 1][j - 1][3 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[7 - 1][j - 1][2 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               6 - 1]

                    self.model.addCons(sum4 <= 2)

                    sum5 = self.ans[4 - 1][j - 1][3 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[6 - 1][j - 1][2 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[7 - 1][j - 1][1 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               2 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               2 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1]

                    self.model.addCons(sum5 <= 2)

                    sum6 = self.ans[4 - 1][j - 1][2 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               1 - 1] + \
                           self.ans[6 - 1][j - 1][1 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[7 - 1][j - 1][6 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[8 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               6 - 1]

                    self.model.addCons(sum6 <= 2)

                elif len(self.ans) >= 7:
                    sum1 = self.ans[4 - 1][j - 1][3 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               2 - 1] + \
                           self.ans[6 - 1][j - 1][2 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               1 - 1] + \
                           self.ans[7 - 1][j - 1][1 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               6 - 1]

                    self.model.addCons(sum1 <= 2)

                    sum2 = self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1]

                    self.model.addCons(sum2 <= 2)

                    sum3 = self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               1 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               5 - 1]

                    self.model.addCons(sum3 <= 2)

                    sum4 = self.ans[4 - 1][j - 1][4 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[6 - 1][j - 1][3 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[7 - 1][j - 1][2 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               3 - 1]

                    self.model.addCons(sum4 <= 2)

                    sum5 = self.ans[4 - 1][j - 1][3 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[6 - 1][j - 1][2 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               3 - 1] + \
                           self.ans[7 - 1][j - 1][1 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               2 - 1]

                    self.model.addCons(sum5 <= 2)

                    sum6 = self.ans[4 - 1][j - 1][2 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               1 - 1] + \
                           self.ans[6 - 1][j - 1][1 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[7 - 1][j - 1][6 - 1] + \
                           self.ans[7 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1]

                    self.model.addCons(sum6 <= 2)

                else:
                    sum1 = self.ans[4 - 1][j - 1][3 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               2 - 1] + \
                           self.ans[6 - 1][j - 1][2 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               1 - 1]

                    self.model.addCons(sum1 <= 2)

                    sum2 = self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1]

                    self.model.addCons(sum2 <= 2)

                    sum3 = self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               6 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               1 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 1, chosen_field[1]) - 1][
                               6 - 1]

                    self.model.addCons(sum3 <= 2)

                    sum4 = self.ans[4 - 1][j - 1][4 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               5 - 1] + \
                           self.ans[6 - 1][j - 1][3 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               4 - 1]

                    self.model.addCons(sum4 <= 2)

                    sum5 = self.ans[4 - 1][j - 1][3 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               4 - 1] + \
                           self.ans[6 - 1][j - 1][2 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 3, chosen_field[1]) - 1][
                               3 - 1]

                    self.model.addCons(sum5 <= 2)

                    sum6 = self.ans[4 - 1][j - 1][2 - 1] + \
                           self.ans[4 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               1 - 1] + \
                           self.ans[6 - 1][j - 1][1 - 1] + \
                           self.ans[6 - 1][sub_functions.choose_a_function(is_spiral, j, 2, chosen_field[1]) - 1][
                               6 - 1]

                    self.model.addCons(sum6 <= 2)

