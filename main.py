import random
from ursina import *
from ursina.prefabs.platformer_controller_2d import PlatformerController2d

app = Ursina()

# ОКНО

# размер полного экрана = разрешение монитора
window.fullscreen_size = Vec2(window.screen_resolution[0], window.screen_resolution[1])

# включаем полный экран
window.fullscreen = True

# цвет фона окна
# TODO: выделить цвета в переменные или в словарь
window.color = color.color(240, 0.5, 0.7)

# ФУНКЦИИ РИСОВАНИЯ
# Мир состоит из вертикальных колонн
# Колонны состоят квадратных блоков (в несколтько слоев)
# 1-й слой (нижний) – камни – случайное число
# 2-й слой – земля – 3 блока
# 3-й слой – трава – 1 блок 

def draw_world(columns_amount, start_x, start_y):
    """
        Рисует горизонтальный ряд из колонн
        Первая колонна рисуется из start_x, start_y высотой first_column_height

        columns_amount – количество колонн
        start_x – x нижнего блока первой колонны
        start_y – y нижнего блока первой колонны
        first_column_height – высота первой колонны
    """

    # first_column_height задается один раз за весь мир
    # от нее зависит высота следующих колонн
    first_column_height = random.randint(5, 8)
    for i in range(columns_amount):
        draw_column(first_column_height, start_x, start_y)
        # ограничим минимальную высоту колонны одним блоком
        if first_column_height < 2:
            first_column_height += random.randint(0, 1)
        else:
            first_column_height += random.randint(-1, 1)
        # смещаемся вправо перед рисованием следующей колонны
        start_x += 1

def draw_column(first_column_height, start_x, start_y):
    """
        Рисует колонну из блоков.

        first_column_height – высота первой колонны
        start_x – x первого (нижнего) блока в колонне
        start_y – y первого (нижнего) блока в колонне

        TODO: выделить рисование блока в функцию
        TODO: сделать счетчик блоков
        TODO: посчитать время рисования мира
    """

    # 1-й слой колонны – камни
    for i in range(first_column_height):
        block = Entity(
            model="quad",
            collider="box",
            color=color.color(0, 0, .5),
            scale=(1, 1),
            x=start_x,
            y=start_y,
        )
        # смещаемся выше для рисования следующего блока
        start_y += 1

    # 2-й слой колонны – 3 блока земли
    for i in range(3):
        block = Entity(
            model="quad",
            collider="box",
            color=color.color(50, .38, .72),
            scale=(1, 1),
            x=start_x,
            y=start_y,
        )
        start_y += 1

    # 3-й слой колонны – 1 блок травы
    block = Entity(
        model="quad",
        collider="box",
        color=color.color(120, .5, .7),
        scale=(1, 1),
        x=start_x,
        y=start_y,
    )


# рисуем мир в 50 колонн из x 0, y 0
draw_world(50, 0, 0)

# создаем игрока в x 0 и y 15
# TODO: определить точку появления игрока по последнему (верхнему) блоку в первой колонне
player = PlatformerController2d(
    collision=True,
    position=(0, 15),
)

# КАМЕРА

# поле зрения (field of view) камеры
# больше значение – больше объектов видно одновременно
camera.fov = 20

# отключаем перспективу
# model = "cube" будет плоским
camera.orthographic = True

# сразу переходим на игрока чтобы не ждать, пока камера до него доедет
camera.position = player.position

# камера преследует игрока
# смещение камеры относительно игрока [по x 0, по y 5, по z -2]
# смещение по z < - 1, иначе игрока не видно
# скорость камеры 8
camera.add_script(SmoothFollow(target=player, offset=[0, 5, -2], speed=8))

# ФУНКЦИИ УРСИНЫ, ВЫЗЫВАЮТСЯ САМИ

# вызывается постоянно, можно зажимать клавиши
# если нажата клавиша, возвращается 1, если нет – 0
# time.dt – время с последнего кадра
def update():
    camera.fov += held_keys["2"] * time.dt * 10
    camera.fov -= held_keys["8"] * time.dt * 10

# вызывается по нажатию клавиши, нельзя зажимать
def input(key):
    # выход
    if key == "escape":
        sys.exit()

    # вернуть игрока на начало
    if key == "enter":
        player.position = (0, 20)

# запускаем игру
app.run()
