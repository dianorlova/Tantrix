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
