from matplotlib import pyplot as plt
import math
import numpy as np


# координаты точки подвеса камеры
x_0 = 0
y_0 = 0
z_0 = 10

beta = math.radians(0)  # угол скольжения
teta_x = math.radians(13)  # угол захвата камеры по оси Х
teta_y = math.radians(10)  # угол захвата камеры по оси y

# начальные значения при alfa=0
def position_camera_is_alfa_zero(beta):
    x_A_0 = x_0 - math.tan(teta_x/2) * z_0 / np.cos(beta)
    y_A_0 = y_0 + np.tan(beta) * z_0

    x_B_0 = x_0 + math.tan(teta_x/2) * z_0 / np.cos(beta)
    y_B_0 = y_0 + np.tan(beta) * z_0

    x_C_0 = x_0 + np.tan(teta_x/2) * z_0 / np.cos(beta+teta_y)
    y_C_0 = y_0 + np.tan(beta+teta_y) * z_0

    x_D_0 = x_0 - np.tan(teta_x/2) * z_0 / np.cos(beta+teta_y)
    y_D_0 = y_0 + np.tan(beta+teta_y) * z_0

    return x_A_0, x_B_0, x_C_0, x_D_0, y_A_0, y_B_0, y_C_0, y_D_0


def draw_quadrangle(x_A, x_B, x_C, x_D, y_A, y_B, y_C, y_D, color='black', linewidth=0.5):

    x = [x_A, x_B, x_C, x_D, x_A]
    x = np.array(x)
    y = [y_A, y_B, y_C, y_D, y_A]
    y = np.array(y)
    plt.plot(x, y, color=color, alpha=0.7,
        linewidth=linewidth, solid_capstyle='round', zorder=2)
    plt.pause(0.05)


def rotate(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.
    The angle should be given in radians.

    функция rotate выполняет поворот точки point на угол angle (против часовой стрелки, в радианах) вокруг origin,
    в декартовой плоскости, с обычными условными обозначениями оси: x, увеличивающийся слева справа, y увеличиваясь
    вертикально вверх. Все точки представлены как длина-2 кортежа формы (x_coord, y_coord).
    """
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)

    return qx, qy


def decart2alfa(x_A, x_B, x_C, x_D, y_A, y_B, y_C, y_D, alfa):
    point_A = x_A, y_A
    point_B = x_B, y_B
    point_C = x_C, y_C
    point_D = x_D, y_D
    origin = x_0, y_0

    rot_A_x, rot_A_y = rotate(origin, point_A, alfa)
    rot_B_x, rot_B_y = rotate(origin, point_B, alfa)
    rot_C_x, rot_C_y = rotate(origin, point_C, alfa)
    rot_D_x, rot_D_y = rotate(origin, point_D, alfa)

    return rot_A_x, rot_A_y, rot_B_x, rot_B_y, rot_C_x, rot_C_y, rot_D_x, rot_D_y


# plt.axis([-25, 25, -5, 45])
# plt.figure()
fig, axs = plt.subplots()
plt.plot((-10,10), (0,0), 'black')

x_A_0, x_B_0, x_C_0, x_D_0, y_A_0, y_B_0, y_C_0, y_D_0 = position_camera_is_alfa_zero(beta)
# draw_quadrangle(x_A_0, x_B_0, x_C_0, x_D_0, y_A_0, y_B_0, y_C_0, y_D_0)

# угол поворота камеры на различных beta для обеспечения требуемого перекрвтия
# steps_alfa = 60, 29, 25, 20, 16, 14, 13, 12
# количество поворотов на различных beta для обеспечения требуемого перекрытия и равенства крайних положений камеры
num_steps_alfa = 4, 8, 11, 14, 16, 20, 22, 26
i = -1


for beta in range(0, 61, 8):
    i += 1
    # print('beta ', beta)
    beta = math.radians(beta)
    x_A_0, x_B_0, x_C_0, x_D_0, y_A_0, y_B_0, y_C_0, y_D_0 = position_camera_is_alfa_zero(beta)
    # step_alfa = int(steps_alfa[i])
    angle_alfa = np.linspace(-85, 175, num_steps_alfa[i])
    # print('steps_alfa ', step_alfa)
    for angle in angle_alfa:#range(-85, 95, step_alfa):
        # print('angle ', step_alfa)
        alfa = math.radians(angle)
        x_A, y_A, x_B, y_B, x_C, y_C, x_D, y_D = decart2alfa(x_A_0, x_B_0, x_C_0, x_D_0, y_A_0, y_B_0, y_C_0, y_D_0, alfa)

        draw_quadrangle(x_A, x_B, x_C, x_D, y_A, y_B, y_C, y_D, color='red')
        draw_quadrangle(x_A, x_B, x_C, x_D, y_A, y_B, y_C, y_D, color='black')

img = plt.imread('xp1.jpg')
shift_ver = -15
shift_gor = -49
axs.imshow(img, extent=[0 + shift_gor, 80 + shift_gor, 0 + shift_ver, 40 + shift_ver])  # 80, 40
# plt.axis([-25, 25, -25, 25])

plt.grid(True)
plt.show()