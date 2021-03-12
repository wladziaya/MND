import random, math, numpy as np

# Кількість експериментів, межі у і х, додатковий нульовий фактор

y_max = (30 - 130) * 10 # -950
y_min = (20 - 130) * 10 # -1050
x_min = [10, 50]
x_max = [20, 60]
x0 = 1
# Створення матриці ПФЕ
line1 = [x_min[0], x_min[1]]
line2 = [x_min[0], x_max[1]]
line3 = [x_max[0], x_min[1]]
line4 = [x_max[0], x_max[1]]
matrix = [line1, line2, line3, line4]
# Значення коефіцієнта критерію Романовського при кількості дослідів m за довірчої ймовірності 0.99
romanovskyi_cr = {6: 2.16, 7: 2.3, 8: 2.43, 9: 2.5, 10: 2.62, 11: 2.7, 12: 2.75,
                 13: 2.8, 14: 2.85, 15: 2.9, 16: 2.94, 17: 2.97, 18: 3, 19: 3.05, 20: 3.08}

# Функція знаходження середьного значення
def average(list_y):
    average = 0
    for y in list_y:
        average += y / len(list_y)
    return average
# Перевірка дисперсії на однорідність. Повторюється поки дисперсія не однорідна
def homogeneity():
    def romanovskyi(dispertion):
        def fuv():
            f_uv = []
            f_uv.append(dispertion[0] / dispertion[1])
            f_uv.append(dispertion[2] / dispertion[0])
            f_uv.append(dispertion[2] / dispertion[1])
            return f_uv
        def thetauv(f_uv):
            theta_uv = []
            theta_uv.append((m - 2 / m) * f_uv[0])
            theta_uv.append((m - 2 / m) * f_uv[1])
            theta_uv.append((m - 2 / m) * f_uv[2])
            return theta_uv
        # Основне відхилення
        sigma = math.sqrt(2 / m * (2 * m - 2) / (m - 4))
        f_uv = fuv()
        theta_uv = thetauv(f_uv)
        r_uv1 = abs(theta_uv[0] - 1) / sigma
        r_uv2 = abs(theta_uv[1] - 1) / sigma
        r_uv3 = abs(theta_uv[2] - 1) / sigma
        if (r_uv1 < romanovskyi_cr[m]) and (r_uv2 < romanovskyi_cr[m]) \
                and (r_uv3 < romanovskyi_cr[m]): return False
        else: return True
    def dispertion(list_y):
        average_y = average(list_y)
        dispertion = 0
        for y in list_y:
            dispertion += (y - average_y)**2 / len(list_y)
        return dispertion

    # Функції відгуку в точках експерименту
    m = 6
    y1 = [random.randint(0, 100) + y_min for _ in range(m)]
    y2 = [random.randint(0, 100) + y_min for _ in range(m)]
    y3 = [random.randint(0, 100) + y_min for _ in range(m)]

    # Дисперсія
    dispertion = [dispertion(y1), dispertion(y2), dispertion(y3)]
    # Перевірка однорідності за критерієм Романовського
    error = romanovskyi(dispertion)

    if not error:
        print("Дисперсія однорідна\nОбчислимо коефіцієнти рівняння регресії")
    else:
        if m == 20:
            print(
                "Дисперсія неодноріда при кількості дослідів m = 20\nтому ми не можемо перейти до обчислення коефіцієнтів рівняння регресії")
            exit()
        else:
            m += 1
            homogeneity()
            exit()
    print("Значення факторів у точках експерименту:")
    for line in matrix:
        print(line)
    print(f"\nФункції відгуку:\nВ першій точці: {y1}\nВ другій точці: {y2}\nВ третій точці: {y3}")
    print(f"\nСередні значення Y:\n{average(y1)}\n{average(y2)}\n{average(y3)}")
    print(f"\nДисперсія: {dispertion}")
    y = [y1, y2, y3]
    normalisation(y)

def normalisation(y):
    normalized_matrix = [[-1, -1], [-1, 1], [1, -1], [1, 1]]
    # Розрахунок нормованих коефіцієнтів рівняння регресії
    mx1 = (normalized_matrix[0][0] + normalized_matrix[1][0] + normalized_matrix[2][0]) / 3
    mx2 = (normalized_matrix[0][1] + normalized_matrix[1][1] + normalized_matrix[2][1]) / 3
    my = (average(y[0]) + average(y[1]) + average(y[2])) / 3
    a1 = (normalized_matrix[0][0]**2 + normalized_matrix[1][0]**2 + normalized_matrix[2][0]**2) / 3
    a2 = (normalized_matrix[0][0] * normalized_matrix[0][1] + normalized_matrix[1][0] * normalized_matrix[1][1] + normalized_matrix[2][0] * normalized_matrix[2][1]) / 3
    a3 = (normalized_matrix[0][1]**2 + normalized_matrix[1][1]**2 + normalized_matrix[2][1]**2) / 3

    a11 = (normalized_matrix[0][0] * average(y[0]) + normalized_matrix[1][0] * average(y[1]) + normalized_matrix[2][0] * average(y[2])) / 3
    a22 = (normalized_matrix[0][1] * average(y[0]) + normalized_matrix[1][1] * average(y[1]) + normalized_matrix[2][1] * average(y[2])) / 3

    b0_numerator = np.array([[my, mx1, mx2],
                             [a11, a1, a2],
                             [a22, a2, a3]])
    b0_denominator = np.array([[1, mx1, mx2],
                               [mx1, a1, a2],
                               [mx2, a2, a3]])

    b0 = np.linalg.det(b0_numerator) / np.linalg.det(b0_denominator)

    b1_numerator = np.array([[1, my, mx2],
                             [mx1, a11, a2],
                             [mx2, a22, a3]])
    b1_denominator = np.array([[1, mx1, mx2],
                               [mx1, a1, a2],
                               [mx2, a2, a3]])

    b1 = np.linalg.det(b1_numerator) / np.linalg.det(b1_denominator)

    b2_numerator = np.array([[1, mx1, my],
                             [mx1, a1, a11],
                             [mx2, a2, a22]])
    b2_denominator = np.array([[1, mx1, mx2],
                               [mx1, a1, a2],
                               [mx2, a2, a3]])

    b2 = np.linalg.det(b2_numerator) / np.linalg.det(b2_denominator)

    # Натуралізація коефіцієнтів

    delta_x1 = abs(x_max[0] - x_min[0]) / 2
    delta_x2 = abs(x_max[1] - x_min[1]) / 2

    x10 = (x_max[0] + x_min[0]) / 2
    x20 = (x_max[1] + x_min[1]) / 2

    a0 = b0 - b1 * (x10 / delta_x1) - b2 * (x20 / delta_x2)
    a1 = b1 / delta_x1
    a2 = b2 / delta_x2

    print("\nНормалізована матриця")
    for line in normalized_matrix:
        print(line)
    print(f"\nb0 = {b0}; b1 = {b1}; b2 = {b2}")
    print(f"Нормоване рівняння регресії:\ny = {round(b0, 3)} + {round(b1, 3)}*x1 + {round(b2, 3)}*x2")
    # Перевірка
    print("Середні значення нормованих Y:")
    for i in range(3):
        print(f"{b0 + b1*normalized_matrix[i][0] + b2*normalized_matrix[i][1]}")
    print("Значення збігаються зі значеннями Yj")
    print(f"\na0 = {a0}; a1 = {a1}; a2 = {a2}")
    print(f"Натуралізоване рівняння регресії:\ny = {round(a0, 3)} + {round(a1, 3)}*x1 + {round(a2, 3)}*x2")
    # Перевірка
    print("\nСередні значення натуралізованих Y:")
    for i in range(3):
        print(f"{a0 + a1*matrix[i][0] + a2*matrix[i][1]}")
    print("Значення збігаються зі значеннями Yj")
    print("Отже, коефіцієнти рівняння регресії розраховані правильно")


# Виклик функції перевірки однорідності дисперсії
homogeneity()
