def create_structure(n, sub_functions):
    """
    Создаёт следующую структуру(словарь) данных:
    {Ячейка 1:
       {Ребро 1:Номер соседа, ..., Ребро 6:Номер соседа},
     Ячейка 2:{...},
     ...,
     Ячейка n:{...}}

     и записывает её в файл graph.txt

     Принимает:
        n - количество фишек
        sub_functions - объект класса SubFunctions
    """
    graph = {}

    file = open('graph.txt', 'w', encoding='utf-8')
    file.write(f'{{\n')  # экранируем '{' путём удвоения

    graph.fromkeys(list(range(1, n + 1)))  # заполняем словарь ключами - номерами ячеек(мест)
    for i in range(1, n + 1):
        dict_rib_neighbor = {}  # словарь ребро-сосед
        graph[i] = dict_rib_neighbor.fromkeys(
            list(range(1, 7)))  # для каждой ячейки есть свой словарь с ребрами-соседями
        for l in range(1, 7):
            dict_rib_neighbor[l] = sub_functions.a(i, l)  # ребро(ключ): сосед(значение)
            graph[i][l] = dict_rib_neighbor[l]

        file.write(f'  {i}:\n\t{graph[i]}\n')

    file.write(f'}}')  # экранируем '}' путём удвоения
    file.close()