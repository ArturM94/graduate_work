"""
Diffusion from the point source

Программа представляет собой решение задачи диффузии загрязнений в атмосфере
методом конечных разностей (явная схема) для двумерной области решений,
используя уравнение теплопроводности c добавлением слогаемого Q (источник
загрязнения). Результатом программы является тепловая карта (heatmap)
концентраций загрязнений в точках двумерного массива.

Author: Artur Manukian
"""

import numpy as np
import matplotlib.pylab as plt


class Diffusion:

    size_grid = 40  # Размер сетеки.
    n = 100  # Количество итераций.
    t = 0  # Граничное условие первого рода (температура).
    T = []  # Временной слой.
    new_T = []  # Новый временной слой.
    # Значения
    # lambda - теплопроводность,
    # ro - плотность,
    # c - теплоемкость,
    # tau - шаг по времени
    # заданы для температуры 30 градусов Цельсия.
    lamda = 0.0267
    ro = 1.165
    c = 1005
    tau = 0.01
    h = 0  # Шаг п осетке.
    stability = 0  # Условие устойчивости схемы.

    # Концентрация и координаты для одного источника
    x_chimney = 20
    y_chimney = 20
    Q = 2

    # Выполнение условия устойчивости
    while tau >= stability:
        stability = (ro * c * h ** 2) / (2 * lamda)
        h += 0.0005
        # print(stability, h)

    # Заполнение сетки нулевыми значениями
    # T = [[0 for j in range(size_grid)] * size_grid for i in range(size_grid)]
    # for i in range(size_grid):
    #     for j in range(size_grid):
    #         T[i][j] = 0
    T = np.zeros((size_grid, size_grid), dtype=float)
    new_T = np.zeros((size_grid, size_grid), dtype=float)

    # Граничные условия
    # Для левой и правой границы.
    for i in range(size_grid):
        T[i][0] = t
        T[i][size_grid - 1] = t
    # Для верхней и нижней границы.
    for j in range(size_grid):
        T[0][j] = t
        T[size_grid - 1][j] = t
    # Сетка с граничными условиями
    for i in range(size_grid):
        for j in range(size_grid):
            # Дублирование начальных значений для нового временного слоя.
            new_T[i][j] = T[i][j]

    # Уравнение диффузии для одного источника
    for counter in range(n):
        for i in range(size_grid - 1):
            for j in range(size_grid - 1):
                # Источник загрязнения.
                if i == y_chimney and j == x_chimney:
                    T[i][j] = new_T[i][j] + ((lamda * tau) / (ro * c) *
                                             ((new_T[i + 1][j] +
                                               new_T[i - 1][j] +
                                               new_T[i][j + 1] +
                                               new_T[i][j - 1] - 4 *
                                               new_T[i][j]) /
                                              h ** 2)) + Q
                else:
                    T[i][j] = new_T[i][j] + ((lamda * tau) / (ro * c) *
                                             ((new_T[i + 1][j] +
                                               new_T[i - 1][j] +
                                               new_T[i][j + 1] +
                                               new_T[i][j - 1] - 4 *
                                               new_T[i][j]) /
                                              h ** 2))
        # Перезапись сетки на новый временной слой.
        for i in range(size_grid - 1):
            for j in range(size_grid - 1):
                new_T[i][j] = T[i][j]

    # Снятие концентрации в точках
    first_point_concentration = T[y_chimney][x_chimney - 3]
    second_point_concentration = T[y_chimney][x_chimney - 6]
    third_point_concentration = T[y_chimney][x_chimney - 9]
    print(f'Концентрация в точке 1: {first_point_concentration}')
    print(f'Концентрация в точке 2: {second_point_concentration}')
    print(f'Концентрация в точке 3: {third_point_concentration}')

    # Исходные данные
    print(f'Условие устойчивости схемы: {stability}')
    print(f'lambda: {lamda}')
    print(f'ro: {ro}')
    print(f'c: {c}')
    print(f'tau: {tau}')
    print(f'h: {h}')

    # Вывод сетки в консоль
    plt.imshow(new_T, cmap='Greys')
    plt.show()
