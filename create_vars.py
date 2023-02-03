class CreateVars:
    """
        Описывает добавление переменных x(i,j,k) и  y(j,l) в модель
    """

    def __init__(self, n, n_new, ans, model, colors_list):
        self.n = n
        self.n_new = n_new
        self.ans = ans
        self.model = model
        self.colors_list = colors_list

    def create_x_i_j_k(self):
        """
        x_i_j_k = 1, если фишка i помещена на место j с ориентацией k,
        x_i_j_k = 0, если фишка i не помещена на место j с ориентацией k
        """
        count_x_i_j_k = 0
        file = open('x_i_j_k-output.txt', 'w', encoding='utf-8')
        for i in range(1, self.n_new + 1):
            self.ans.append(list())
            for j in range(1, self.n + 1):
                self.ans[i - 1].append(list())
                for k in range(1, 7):
                    self.ans[i - 1][j - 1].append(self.model.addVar(f"x_{i}_{j}_{k}", vtype="INTEGER"))
                    self.model.addCons(0 <= (self.ans[i - 1][j - 1][k - 1] <= 1))  # x_i_j_k принимает значение 1 или 0

                    count_x_i_j_k += 1
                    file.write(f'{self.ans[i - 1][j - 1][k - 1]}\n')

        file.write(f'Переменных x_i_j_k: {count_x_i_j_k}')
        file.close()

    def create_y_j_l(self):
        """
        Выражает цвет линии соответствующего ребра l места j,
        y_j_l = 1,
        y_j_l = 2,
        y_j_l = 3 (обозначенный цвет)
        """
        count_y_j_l = 0
        file = open('y_j_l-output.txt', 'w', encoding='utf-8')
        for j in range(1, self.n + 1):
            self.colors_list.append(list())
            for l in range(1, 7):
                self.colors_list[j - 1].append(self.model.addVar(f"y_{j}_{l}", vtype="INTEGER"))
                self.model.addCons(1 <= (self.colors_list[j - 1][l - 1] <= 3))  # y_j_l принимает значение 1, 2 или 3

                count_y_j_l += 1
                file.write(f'{self.colors_list[j - 1][l - 1]}\n')

        file.write(f'Переменных y_j_l: {count_y_j_l}')
        file.close()
