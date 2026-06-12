import tkinter as tk
import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class Bullet:
    def __init__(self, canvas, x, y, direction, size=8, speed=10, owner=None):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.direction = direction
        self.size = size
        self.speed = speed
        self.owner = owner
        self.game_frame = None
        self.id = None

        # загрузка текстуры пули

        self.texture = tk.PhotoImage(file=resource_path("frame/images/bullet.png"))

        self.draw()
        self.move()

    def draw(self):
        if self.id:
            self.canvas.delete(self.id)

        if self.texture:
            self.id = self.canvas.create_image(self.x, self.y, image=self.texture, anchor="center")
        else:
            x1 = self.x - self.size // 2
            y1 = self.y - self.size // 2
            x2 = self.x + self.size // 2
            y2 = self.y + self.size // 2
            self.id = self.canvas.create_rectangle(x1, y1, x2, y2, fill="yellow", outline="orange")

    def move(self):
        if self.direction == "up":
            self.y -= self.speed
        elif self.direction == "down":
            self.y += self.speed
        elif self.direction == "left":
            self.x -= self.speed
        elif self.direction == "right":
            self.x += self.speed

        self.draw()

        # проверка выхода за границы
        if self.x < 0 or self.x > self.canvas.winfo_width() or self.y < 0 or self.y > self.canvas.winfo_height():
            self.destroy()
            return

        if self.check_collision():
            return

            # продолжение движения
        self.canvas.after(30, self.move)

    def destroy(self):
        if self.id:
            self.canvas.delete(self.id)

    def get_position(self):
        return self.x, self.y

    def check_collision(self):
        #Проверка столкновения с блоками
        if self.game_frame is None:
            return False

        gf = self.game_frame

        col = int(self.x // gf.cell_size)
        row = int(self.y // gf.cell_size)

        # проверка границ
        if col < 0 or col >= gf.map_width or row < 0 or row >= gf.map_height:
            self.destroy()
            return True

        # проверка стали
        if (col, row) in gf.steel_blocks:
            self.destroy()
            return True
        if (col, row) == gf.eagle_position:
            gf.eagle_destroyed()
            self.destroy()
            return True

        # проверка кирпичей
        if (col, row) in gf.brick_blocks:
            gf.brick_blocks.remove((col, row))
            gf.canvas.delete(f"brick_{col}_{row}")
            self.destroy()
            return True
        if self.owner != gf.player_tank and gf.player_tank and gf.player_tank.is_alive:
            px, py = gf.player_tank.get_position()
            distance = ((self.x - px) ** 2 + (self.y - py) ** 2) ** 0.5
            if distance < gf.cell_size // 2:
                gf.lose_life()
                self.destroy()
                return True
        for enemy in gf.enemies[:]:
            if enemy is self.owner:  # пропускаем того, кто выстрелил
                continue

            ex, ey = enemy.get_position()
            # проверка по расстоянию
            distance = ((self.x - ex) ** 2 + (self.y - ey) ** 2) ** 0.5
            if distance < gf.cell_size // 2:  # радиус попадания 20px
                gf.score_system.add_points(100)
                gf.update_score_display()
                enemy.destroy()
                gf.enemies.remove(enemy)
                gf.enemies_killed += 1
                self.destroy()

                if gf.enemies_killed >= gf.enemies_total:
                    gf.victory()
                return True

        return False