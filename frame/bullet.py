import tkinter as tk


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

        self.texture = tk.PhotoImage(file="frame/images/bullet.png")

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
        """Проверка столкновения с блоками через GameFrame"""
        if self.game_frame is None:
            print("game_frame = None")  # отладка
            return False

        gf = self.game_frame

        col = int(self.x // gf.cell_size)
        row = int(self.y // gf.cell_size)

        print(f"Пуля на клетке: {col}, {row}")  # отладка
        print(f"Кирпичи в этом уровне: {gf.brick_blocks}")  # выводит все кирпичи
        print(f"Сталь в этом уровне: {gf.steel_blocks}")

        # проверка границ
        if col < 0 or col >= gf.map_width or row < 0 or row >= gf.map_height:
            print("Выход за границы")  # отладка
            self.destroy()
            return True

        # проверка стали
        if (col, row) in gf.steel_blocks:
            print("Попала в сталь")  # отладка
            self.destroy()
            return True

        # проверка кирпичей
        if (col, row) in gf.brick_blocks:
            print("Попала в кирпич")  # отладка
            gf.brick_blocks.remove((col, row))
            gf.canvas.delete(f"brick_{col}_{row}")
            self.destroy()
            return True

        print("Нет столкновения")  # отладка
        return False