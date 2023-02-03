def create_y_j_l(n, colors_list, model):
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
