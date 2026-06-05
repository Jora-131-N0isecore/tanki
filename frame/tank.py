import tkinter as tk


class Tank:
    def __init__(self, canvas, x, y, tank_type="player", size=40, speed=3):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.tank_type = tank_type
        self.size = size
        self.speed = speed
        self.direction = "up"
        self.id = None
        self.moving = False
        self.target_x = x
        self.target_y = y

        self.move_up_flag = False
        self.move_down_flag = False
        self.move_left_flag = False
        self.move_right_flag = False

        self.load_textures()
        self.draw()
        self.start_movement()

    def load_textures(self):
        #Загрузка текстур для всех направлений
        prefix = "player_tank" if self.tank_type == "player" else "enemy_tank"

        directions = ["up", "down", "left", "right"]
        self.textures = {}
        for direction in directions:
            self.textures[direction] = tk.PhotoImage(
                file=f"frame/images/{prefix}_{direction}.png"
            )

    def draw(self):
        #Отрисовка танка с учётом направления
        if self.id:
            self.canvas.delete(self.id)

        texture = self.textures[self.direction]
        self.id = self.canvas.create_image(
            self.x, self.y,
            image=texture,
            anchor="center"
        )

    def start_movement(self):
        self.update_position()

    def update_position(self):
        if not self.moving:
            if self.move_up_flag:
                new_y = self.y - self.size
                if self.can_move_to(self.x, new_y):
                    self.target_y = new_y
                    self.direction = "up"
                    self.moving = True
            elif self.move_down_flag:
                new_y = self.y + self.size
                if self.can_move_to(self.x, new_y):
                    self.target_y = new_y
                    self.direction = "down"
                    self.moving = True
            elif self.move_left_flag:
                new_x = self.x - self.size
                if self.can_move_to(new_x, self.y):
                    self.target_x = new_x
                    self.direction = "left"
                    self.moving = True
            elif self.move_right_flag:
                new_x = self.x + self.size
                if self.can_move_to(new_x, self.y):
                    self.target_x = new_x
                    self.direction = "right"
                    self.moving = True


        if self.moving:
            dx = self.target_x - self.x
            dy = self.target_y - self.y

            if abs(dx) < self.speed:
                self.x = self.target_x
            else:
                self.x += self.speed if dx > 0 else -self.speed

            if abs(dy) < self.speed:
                self.y = self.target_y
            else:
                self.y += self.speed if dy > 0 else -self.speed

            if self.x == self.target_x and self.y == self.target_y:
                self.moving = False

            self.draw()

        self.canvas.after(16, self.update_position)

    def can_move_to(self, new_x, new_y):
        #Проверка, может ли танк переместиться в координаты (new_x, new_y)

        # получаем размер карты
        map_width = getattr(self, 'map_width', 15)
        map_height = getattr(self, 'map_height', 15)

        # вычисляеn клетку, куда хочет встать танк
        col = new_x // self.size
        row = new_y // self.size

        # проверка границ
        if col < 0 or col >= map_width or row < 0 or row >= map_height:
            return False

        # проверка на стальные блоки
        steel_blocks = getattr(self, 'steel_blocks', [])
        if (col, row) in steel_blocks:
            return False

        return True

    def start_move_up(self):
        if not self.moving:
            self.move_up_flag = True

    def stop_move_up(self):
        self.move_up_flag = False

    def start_move_down(self):
        if not self.moving:
            self.move_down_flag = True

    def stop_move_down(self):
        self.move_down_flag = False

    def start_move_left(self):
        if not self.moving:
            self.move_left_flag = True

    def stop_move_left(self):
        self.move_left_flag = False

    def start_move_right(self):
        if not self.moving:
            self.move_right_flag = True

    def stop_move_right(self):
        self.move_right_flag = False

    def get_position(self):
        return self.x, self.y

    def get_direction(self):
        return self.direction

    def is_moving(self):
        return self.moving

    def destroy(self):
        if self.id:
            self.canvas.delete(self.id)
