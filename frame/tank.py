import tkinter as tk
import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class Tank:
    def __init__(self, canvas, x, y, tank_type="player", size=40, speed=3):
        self.game_frame = None
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
        self.is_alive = True

        self.move_up_flag = False
        self.move_down_flag = False
        self.move_left_flag = False
        self.move_right_flag = False

        self.load_textures()
        self.draw()
        self.start_movement()

    def load_textures(self):
        #Загрузка текстур для всех направлений
        if self.tank_type == "player":
            prefix = "player_tank"
        else:
            prefix = "enemy_tank"

        directions = ["up", "down", "left", "right"]
        self.textures = {}
        for direction in directions:
            self.textures[direction] = tk.PhotoImage(
                file=resource_path(f"frame/images/{prefix}_{direction}.png")
            )

    def draw(self):
        if not self.is_alive:
            return
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
        if not self.is_alive:
            return
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
            if not self.is_alive:
                return
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
        #Проверка, может ли танк переместиться в новую позицию
        if not hasattr(self, 'game_frame') or self.game_frame is None:
            return True

        gf = self.game_frame

        col = new_x // self.size
        row = new_y // self.size

        # проверка границ карты
        if col < 0 or col >= gf.map_width or row < 0 or row >= gf.map_height:
            return False

        # проверка стали
        if (col, row) in gf.steel_blocks:
            return False

        # проверка кирпичей
        if (col, row) in gf.brick_blocks:
            return False

        # игрок не наезжает на врагов
        if self.tank_type == "player":
            for enemy in gf.enemies:
                ex, ey = enemy.get_position()
                ecol = ex // self.size
                erow = ey // self.size
                if (col, row) == (ecol, erow):
                    return False

        # враг не наезжает на игрока и на других врагов
        if self.tank_type == "enemy":
            if gf.player_tank and gf.player_tank.is_alive:
                px, py = gf.player_tank.get_position()
                pcol = px // self.size
                prow = py // self.size
                if (col, row) == (pcol, prow):
                    return False

            for enemy in gf.enemies:
                if enemy is self:
                    continue
                ex, ey = enemy.get_position()
                ecol = ex // self.size
                erow = ey // self.size
                if (col, row) == (ecol, erow):
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
        self.is_alive = False
        if self.id:
            self.canvas.delete(self.id)
            self.id = None
