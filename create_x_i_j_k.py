def create_x_i_j_k(n,n_new,ans,model):
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