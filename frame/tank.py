import tkinter as tk


class Tank:
    def __init__(self, canvas, x, y, tank_type="player", size=40, speed=8):
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
                file=f"images/{prefix}_{direction}.png"
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
                self.target_y = self.y - self.size
                self.direction = "up"
                self.moving = True
            elif self.move_down_flag:
                self.target_y = self.y + self.size
                self.direction = "down"
                self.moving = True
            elif self.move_left_flag:
                self.target_x = self.x - self.size
                self.direction = "left"
                self.moving = True
            elif self.move_right_flag:
                self.target_x = self.x + self.size
                self.direction = "right"
                self.moving = True
            self.draw()

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
