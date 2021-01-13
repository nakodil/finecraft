import sys
import tilemap
from ursina import *
from ursina.prefabs.platformer_controller_2d import PlatformerController2d


app = Ursina()

window.title = 'My Game'
window.borderless = False
window.fullscreen = True
window.exit_button.visible = False
window.fps_counter.enabled = True

camera.orthographic = True
camera.fov = 10


# diag = Button(text='placeholder', scale=.1, origin_y=-3)


class Player(PlatformerController2d):
    def __init__(self):
        super().__init__(
            position=Vec3(3, 20, 0),
            color=color.orange,
        )


class Tile(Entity):
    def __init__(self, x_shift, y_shift, block_color):
        super().__init__(
            model='cube',
            position=Vec3(x_shift, y_shift, 0),
            scale=(1, 1, 1),
            collider='box',
        )

        if block_color == "g":
            self.color = color.rgba(124, 141, 76, a=255)
        elif block_color == "s":
            self.color = color.rgba(114, 84, 40, a=255)
        elif block_color == "r":
            self.color = color.rgba(150, 159, 178, a=255)
        elif block_color == "w":
            self.color = color.rgba(182, 227, 219, a=150)
            self.collider = None


player = Player()
camera.add_script(SmoothFollow(target=player, offset=[0, 1, -30], speed=20))

controls = """
            A, D – двигаться
            Q, E – приблизиться 
            SPACE – прыгнуть
            ENTER – вернуться
            ESC – выйти
        """

text1 = Text(
    text = controls,
    parent = scene,
    scale = 20,
    x = 0,
    y = 5,
    z = 0,
)

# TILES
# TODO turn matrix 90 ccw
tiles = []
row_counter = 0
for i in tilemap.data:
    element_counter = 0
    for j in str(i):
        if j != " ":
            tile = Tile(element_counter, row_counter, j)
            tiles.append(tile)
        element_counter += 1

    row_counter -= 1


# CONTROLS
def update():
    if held_keys['escape']:
        sys.exit()

    if held_keys['enter']:
        player.position = Vec3(3, 20, 0)

    if held_keys['q']:
        camera.fov += 1

    if held_keys['e']:
        camera.fov -= 1


if __name__ == '__main__':
    app.run()
