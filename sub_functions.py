# импорты словарей с цветами линий
from dict_designated_color import dict_designated_color
from dict_colors import dict_colors
from dict_chip_orientation_edge import dict_chip_orientation_edge

# Показывает шаг, на который нужно сместиться по выбранному ребру с текущего места, чтобы перейти на новое место
# см. картинку https://github.com/stephanh42/hexutil/blob/master/img/hexcoords.png
step = {
    1: (2, 0),
    2: (1, 1),
    3: (-1, 1),
    4: (-2, 0),
    5: (-1, -1),
    6: (1, -1)
}   # для спирали


class SubFunctions:

    def __init__(self, n):
        self.ans_to, self.ans_from = self.find_all_coordinates(n)
        self.n = n

    def bias(self, current_location, l):
        """
        Вычисление координат нового места, на которое сместились по ребру l

        Принимает:
            current_location - номер текущего места,
            l - номер ребра текущего места

        Возвращает:
            Координаты нового места, на которое сместились по ребру l
        """
        x, y = current_location
        dx, dy = step[l]
        return x + dx, y + dy

    def find_all_coordinates(self, n):
        """
        Возвращает:
        Словарь ans_to с номерами мест и их координатами на доске,
        Словарь ans_from, аналог ans_to, ключ-значение поменяны местами.
        """
        sp_num = 1  # номер шага в спирали (или номер ячейки на поле)
        start = (0, 0)
        ans_to = {}  # словарь, где 'ключ' - номер места(от 1 до n), 'значение' - координаты этого места на доске
        ans_from = {}  # аналогично, но 'ключ' и 'значение' поменяны местами (для удобства)
        i = 1
        while True:
            # l проходит по всем рёбрам в спирали
            for l in ([6] * max(0, i - 2) + [1] * (i - 1) + [2] * (i - 1) + [3] * (i - 1) + [4] * (i - 1) + [5] * i):
                if sp_num > n:
                    return ans_to, ans_from
                ans_to[sp_num] = start
                ans_from[start] = sp_num
                sp_num += 1
                start = self.bias(start, l)
            i += 1

    def choose_a_function(self, is_spiral: bool, j, l, m):
        """В зависимости от формы поля вызывает нужную функцию a"""
        if is_spiral:
            return self.a(j, l)
        return self.a_2(j, l, m)

    def a(self, j, l):
        """
        Функция ищет соседа. Поле в виде спирали.
        Принимает:
            j - номер текущего места,
            l - номер ребра текущего места
        Возвращает:
            Номер места(соседа), смежного с местом j своим краем l,
             и возвращает 0, если такое место находится вне доски.
        """
        return self.ans_from.get(self.bias(self.ans_to[j], l), 0)
        # print(a(7,3)) => 18
        # для места 7 и его ребра 3 есть сосед по этому ребру с местом 18 (см.картинку со спиралью)

    def a_2(self, j, l, m):
        """
        Функция ищет соседа. Поле в виде гексагональной решетки.
        Принимает:
            j - номер текущего места,
            l - номер ребра текущего места,
            m - кол-во мест в строке
        Возвращает:
            Номер места(соседа), смежного с местом j своим краем l,
             и возвращает 0, если такое место находится вне доски.
        """
        j -= 1  # пусть нумерация мест идёт с нуля
        a = j // m  # номер строки (a = 0, 1, 2, ...)
        b = j % m  # номер в строке (b = 1, 2, ..., m)
        ch = a % 2  # четность строки
        n_a = 0  # смещение 'a' в зависимости от ребра l
        n_b = 0  # смещение 'b' в зависимости от ребра l
        if ch != 0:  # если номер строки нечетный
            match l:
                case 1:
                    n_a = a + 0
                    n_b = b + 1
                case 2:
                    n_a = a + 1
                    n_b = b + 1
                case 3:
                    n_a = a + 1
                    n_b = b + 0
                case 4:
                    n_a = a + 0
                    n_b = b - 1
                case 5:
                    n_a = a - 1
                    n_b = b + 0
                case 6:
                    n_a = a - 1
                    n_b = b + 1
        else:  # если номер строки четный
            match l:
                case 1:
                    n_a = a + 0
                    n_b = b + 1
                case 2:
                    n_a = a + 1
                    n_b = b + 0
                case 3:
                    n_a = a + 1
                    n_b = b - 1
                case 4:
                    n_a = a + 0
                    n_b = b - 1
                case 5:
                    n_a = a - 1
                    n_b = b - 1
                case 6:
                    n_a = a - 1
                    n_b = b + 0
        ans = n_a * m + n_b

        # условие на выход за пределы гекс.решетки
        if (ans // m, ans % m) != (n_a, n_b):
            ans = 0
        else:
            ans += 1
        if ans>self.n or ans<1:
            ans = 0
        return ans

    def c(self, i, k, l, n_new):
        """
        Принимает:
            i - номер фишки(от 1 до n_new),
            k - ориентация фишки(от 1 до 6),
            l - ребро(от 1 до 6)
            n_new - n', вид(от 1 до 10) последней фишки из набранных
        Возвращает:
            цвет линии(1,2 или 3), соответствующей ребру l, когда фишка i расположена в ориентации k
        """
        # Исправлено: в этом месте для корректности определения обозначенного цвета перепишем величину n_new,
        # например, если 17 фишек, то обознач. цвет Красный (т.к. цвет фишки вида 17 % 10 = 7 -- Красный)
        # ошибка состояла в том, что по умолчанию n_new = min(n,10), см. ограничение С2 в Дипломе,
        # след-но это давало бы для 17 фишек цвет Синий (min(17,10)=10), что неверно
        if self.n % 10 != 0:    # для корректности обозн. цвета при кол-ве фишек некратном 10
            n_new = self.n % 10

        # получаем обозначенный цвет
        designated_color = dict_designated_color[n_new] # => К,Ж или С

        # получаем словарь цифр цветов по обозначенному цвету
        # например dict_color_indicator = {"К": 3,
        #                                  "Ж": 2,
        #                                  "С": 1}
        dict_color_indicator = dict_colors[designated_color]

        # получаем цвет на ребре l для фишки i в ориентации k
        color = dict_chip_orientation_edge[i][k][l]  # => К,Ж или С
        # получаем цифру этого цвета
        return dict_color_indicator[color]  # => цвет 1,2 или 3

    def get_designated_color(self, n_new):
        # см. выше исправление
        if self.n % 10 != 0:  # для корректности цвета при кол-ве фишек некратном 10
            n_new = self.n % 10

        # получение обозначенного цвета (буква К, Ж или С)
        return dict_designated_color[n_new]

    def loops(self, list_ans, n_new, is_spiral, chosen_field):
        # возвращает список всех циклов(петель) за текущий запуск
        cur_vars = {tuple(i) for i in list_ans}     # {(i,j,k), ..., (i,j,k)} - индексы x_ijk в ответе
        ans = list()
        while cur_vars:     # пока существует cur_vars (или пока не перебрали все переменные x_ijk ответа)
            # находим цикл на нашем решении
            loop = self.get_vars_in_loop(list_ans, n_new, cur_vars.pop(), is_spiral, chosen_field)
            cur_vars -= loop # из множества ijk вычитаем те ijk, которые входят в цикл
            # print(loop)     # выводит цикл на текущем решении (это либо один цикл(петля), либо подцикл)
            ans.append(loop)
        return ans

    def get_vars_in_loop(self, list_ans, n_new, start, is_spiral, chosen_field, designated_color=3):
        """
        Принимает:
            list_ans - Двумерный массив вида [[i, j, k], ..., [i, j, k]], это индексы всех иксов (x_ijk в ответе)
             текущего решения,
            n_new - количество видов фишек (всего может быть 10 видов, т.е. рисунков),
            designated_color - обозначенный цвет (всегда равен 3),
            start - фишка, с которой стартуем и идём по обозначенному цвету designated_color,
            is_spiral - True/False - является ли поле спиралью,
            chosen_field - кортеж с кол-вом строк и столбцов в поле ((0, 0) для спирали)

        Возвращает:
            ans - множество вида {(i,j,k), ..., (i,j,k)}, где ijk - индексы переменных в петле/подцикле
        """
        ans = set()
        dict_j_ijk = dict()
        for lst in list_ans:
            dict_j_ijk[lst[1]] = lst  # d[j] = [i,j,k] для каждого j
        prev = None  # предыдущий
        cur = start  # (i,j,k) текущий (стартовая фишка)
        a = cur[1]  # j из (i,j,k)
        ans.add(tuple(cur))
        while True:
            next_cur = self.get_next(cur, prev, designated_color, dict_j_ijk, n_new, is_spiral, chosen_field)
            if next_cur[1] == a:  # если j соседней фишки = j стартовой фишки => петля замкнулась
                break
            prev = cur[1]  # стартовое место j стало предыдущим
            ans.add(tuple(next_cur))  # (i,j,k) следующей фишки добавляем в множество фишек, входящих в петлю/подцикл
            cur = next_cur  # также смещаем текущую фишку на следующую
        return ans

    def get_next(self, cur, prev, designated_color, dict_j_ijk, n_new, is_spiral, chosen_field):
        # возвращает индексы ijk следующего(соседнего) элемента в петле (ищем соседний эл-т по цвету петли)
        for l in range(1, 7):  # цикл по рёбрам
            cur_color = self.c(cur[0], cur[2], l, n_new)  # получаем текущий цвет ребра (1,2 или 3)
            if cur_color == designated_color:  # если он равен 3 (обозначенному цвету - цвету главной петли)
                next_cur = self.choose_a_function(is_spiral, cur[1], l, chosen_field[1])  # находим соседа в петле для места j=cur[1] по этому ребру l
                if next_cur != prev and next_cur != 0:  # если сосед существует
                    return dict_j_ijk[next_cur]

    @staticmethod
    def number_divisors(n):
        """
        Ищет все делители числа n, кроме делителя 1, т.к. он не нужен(если решетка 1*20, то это полоска из 20 фишек)
        Принимает:
            n - кол-во фишек или мест на поле

        Возвращает:
            список кортежей вида (a,b), где a*b=n; a-длина,b-ширина(высота) решётки
        """
        i = 1
        lst_divisors = list()
        while i <= n ** 0.5:
            if n % i == 0 and i != 1:
                lst_divisors.append((i, n // i))
                if i != (n // i):
                    lst_divisors.append((n // i, i))
            i += 1

        return lst_divisors
