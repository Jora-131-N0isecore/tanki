import tkinter as tk
from .tank import Tank
from .bullet import Bullet
import random

root = tk.Tk()

"""
тут типа крч да словарь так называемый с данными об уровнях пока пустышка потом сделаю
интересно это ктото кроме меня будет читать
"""
levels = {
    1: {"bricks": [(5,5), (5,6), (5,7), (6,5), (6,6), (6,7), (7,5)],
         "steel": [(2,2), (3,2), (4,2), (5,2), (6,2),
                  (2,12), (3,12), (4,12), (5,12), (6,12)],
        "eagle": (10, 10),
        "enemies_total": 10},
    2: {"bricks": [],
        "steel": [(1,1), (2,2)],
        "eagle": (10, 10)},
    3: {"bricks": [], "steel": [], "eagle": (10, 10)},
    4: {"bricks": [], "steel": [], "eagle": (10, 10)},
    5: {"bricks": [], "steel": [], "eagle": (10, 10)},
}


class GameFrame(tk.Frame):
    def __init__(self, parent, level_num, level_data, on_back_callback):
        super().__init__(parent, bg="black")
        self.parent = parent
        self.level_num = level_num
        self.level_data = level_data
        self.on_back_callback = on_back_callback

        # размеры поля
        self.cell_size = 40
        self.map_width = 15
        self.map_height = 15

        # ИНИЦИАЛИЗАЦИЯ СПИСКОВ ДО create_map
        self.brick_blocks = []
        self.steel_blocks = []
        self.bullets = []

        # настройки стрельбы
        self.can_shoot = True
        self.shoot_delay = 1000

        # текстуры
        self.steel_texture = None
        self.brick_texture = None

        self.lives = 3

        # враги
        self.enemies = []
        self.enemies_spawned = 0
        self.enemies_killed = 0
        self.enemies_total = self.level_data.get("enemies_total", 10)
        self.max_enemies = 5
        self.spawn_positions = [(60, 20), (540, 20), (300, 20)]

        self.create_widgets()
        self.load_textures()
        self.create_map()

    def create_widgets(self):
        top_frame = tk.Frame(self, bg="black")
        top_frame.pack(fill="x", pady=5)

        self.lives_label = tk.Label(top_frame, text=f"Жизни: {self.lives}",
                                    font=("Arial", 14), bg="black", fg="red")
        self.lives_label.pack(side="left", padx=20)

        # верхняя панель с информацией
        top_frame = tk.Frame(self, bg="black")
        top_frame.pack(fill="x", pady=5)

        tk.Label(top_frame, text=f"Уровень {self.level_num}",
                 font=("Arial", 14), bg="black", fg="white").pack(side="left", padx=20)

        tk.Button(top_frame, text="Назад в меню",
                  command=self.on_back_callback,
                  bg="gray", fg="white").pack(side="right", padx=20)

        # игровое поле
        self.canvas = tk.Canvas(
            self,
            width=self.map_width * self.cell_size,
            height=self.map_height * self.cell_size,
            bg="darkgreen",
            highlightthickness=0
        )
        self.canvas.pack(pady=20)

        self.canvas.bind_all("<KeyPress-Up>", lambda e: self.player_tank.start_move_up())
        self.canvas.bind_all("<KeyRelease-Up>", lambda e: self.player_tank.stop_move_up())
        self.canvas.bind_all("<KeyPress-Down>", lambda e: self.player_tank.start_move_down())
        self.canvas.bind_all("<KeyRelease-Down>", lambda e: self.player_tank.stop_move_down())
        self.canvas.bind_all("<KeyPress-Left>", lambda e: self.player_tank.start_move_left())
        self.canvas.bind_all("<KeyRelease-Left>", lambda e: self.player_tank.stop_move_left())
        self.canvas.bind_all("<KeyPress-Right>", lambda e: self.player_tank.start_move_right())
        self.canvas.bind_all("<KeyRelease-Right>", lambda e: self.player_tank.stop_move_right())
        self.canvas.bind_all("<space>", lambda e: self.shoot())

        self.canvas.bind_all("<h>", lambda e: self.lose_life())

    def create_map(self):
        # временная сетка для отладки
        for row in range(self.map_height):
            for col in range(self.map_width):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    outline="gray",
                    fill="darkgreen"
                )

        # ИНИЦИАЛИЗАЦИЯ СПИСКОВ (вынеси за пределы циклов!)
        self.brick_blocks = []
        self.steel_blocks = []

        # создание танка
        self.player_tank = Tank(self.canvas, 300, 300, tank_type="player", size=40)
        self.player_tank.game_frame = self
        self.player_tank.map_width = self.map_width
        self.player_tank.map_height = self.map_height

        # отрисовка стали
        for col, row in self.level_data.get("steel", []):
            self.steel_blocks.append((col, row))
            x1 = col * self.cell_size
            y1 = row * self.cell_size
            if self.steel_texture:
                self.canvas.create_image(
                    x1 + self.cell_size // 2,
                    y1 + self.cell_size // 2,
                    image=self.steel_texture,
                    anchor="center"
                )

        # отрисовка кирпичей
        for col, row in self.level_data.get("bricks", []):
            self.brick_blocks.append((col, row))
            x1 = col * self.cell_size
            y1 = row * self.cell_size
            if self.brick_texture:
                self.canvas.create_image(
                    x1 + self.cell_size // 2,
                    y1 + self.cell_size // 2,
                    image=self.brick_texture,
                    anchor="center",
                    tags=(f"brick_{col}_{row}",)
                )
        self.start_enemy_spawn()


    def load_textures(self):
        self.steel_texture = tk.PhotoImage(file="frame/images/steel.png")
        self.brick_texture = tk.PhotoImage(file="frame/images/brick.png")

    def shoot(self):
        if not self.can_shoot:
            return
        if not hasattr(self, 'player_tank') or self.player_tank is None:
            return

        if not hasattr(self, 'player_tank'):
            return

        self.can_shoot = False

        x, y = self.player_tank.get_position()
        direction = self.player_tank.get_direction()

        bullet = Bullet(self.canvas, x, y, direction, owner=self.player_tank)
        bullet.game_frame = self  # передаём ссылку
        self.bullets.append(bullet)

        # таймер для перезарядки
        self.canvas.after(self.shoot_delay, self.reset_shoot)

    def reset_shoot(self):
        self.can_shoot = True

    def respawn_player(self):
        """Возрождает танк игрока после потери жизни"""
        if self.lives <= 0:
            self.game_over()
            return

        # удаляем старый танк
        if hasattr(self, 'player_tank') and self.player_tank:
            self.player_tank.destroy()

        # создаём новый танк в центре
        self.player_tank = Tank(self.canvas, 300, 300, tank_type="player", size=40, speed=3)
        self.player_tank.game_frame = self

        # перепривязываем управление
        self.canvas.bind_all("<KeyPress-Up>", lambda e: self.player_tank.start_move_up())
        self.canvas.bind_all("<KeyRelease-Up>", lambda e: self.player_tank.stop_move_up())
        self.canvas.bind_all("<KeyPress-Down>", lambda e: self.player_tank.start_move_down())
        self.canvas.bind_all("<KeyRelease-Down>", lambda e: self.player_tank.stop_move_down())
        self.canvas.bind_all("<KeyPress-Left>", lambda e: self.player_tank.start_move_left())
        self.canvas.bind_all("<KeyRelease-Left>", lambda e: self.player_tank.stop_move_left())
        self.canvas.bind_all("<KeyPress-Right>", lambda e: self.player_tank.start_move_right())
        self.canvas.bind_all("<KeyRelease-Right>", lambda e: self.player_tank.stop_move_right())

        self.canvas.bind_all("<h>", lambda e: self.lose_life())

        # защита на 1 секунду после респавна
        self.invincible_frames = 60
        self.canvas.after(16, self.update_invincibility)

    def update_lives_display(self):
        """Обновляет отображение жизней на панели"""
        if hasattr(self, 'lives_label'):
            self.lives_label.config(text=f"Жизни: {self.lives}")

    def update_invincibility(self):
        """Обновляет состояние неуязвимости"""
        if hasattr(self, 'invincible_frames') and self.invincible_frames > 0:
            self.invincible_frames -= 1
            # мигание танка (позже добавим)
            self.canvas.after(16, self.update_invincibility)

    def lose_life(self):
        """Потеря одной жизни"""
        self.lives -= 1
        self.update_lives_display()

        if self.lives <= 0:
            self.game_over()
        else:
            # очистить все пули на поле
            for bullet in self.bullets:
                bullet.destroy()
            self.bullets.clear()
            self.respawn_player()

    def game_over(self):
        """Конец игры"""
        if hasattr(self, 'player_tank') and self.player_tank:
            self.player_tank.destroy()

        for enemy in self.enemies:
            enemy.destroy()
        self.enemies.clear()

        for bullet in self.bullets:
            bullet.destroy()
        self.bullets.clear()

        self.canvas.create_text(
            300, 300,
            text="ПОРАЖЕНИЕ...\nНажмите 'Назад в меню'",
            font=("Arial", 24),
            fill="red"
        )

        # очищаем пули
        for bullet in self.bullets:
            bullet.destroy()
        self.bullets.clear()

        # показываем сообщение
        self.canvas.create_text(
            self.canvas.winfo_width() // 2,
            self.canvas.winfo_height() // 2,
            text="ПОРАЖЕНИЕ\nНажмите назад в меню",
            font=("Arial", 24),
            fill="red",
            anchor="center",
            justify="center"
        )

    def start_enemy_spawn(self):
        """Запускает спавн врагов"""
        self.spawn_enemy()
        if self.enemies_killed < self.enemies_total:
            self.canvas.after(3000, self.start_enemy_spawn)

    def spawn_enemy(self):
        """Создаёт одного врага"""
        if self.enemies_killed >= self.enemies_total:
            return
        if self.enemies_spawned >= self.enemies_total:
            return
        if len(self.enemies) >= self.max_enemies:
            return


        x, y = random.choice(self.spawn_positions)

        enemy = Tank(self.canvas, x, y, tank_type="enemy", size=40, speed=2)
        enemy.game_frame = self  # важно!
        enemy.direction = "down"
        enemy.draw()

        self.enemies.append(enemy)
        self.start_enemy_ai(enemy)

        self.enemies_spawned += 1

    def start_enemy_ai(self, enemy):
        """ИИ врага"""


        def ai_loop():
            if enemy not in self.enemies:
                return

            if not enemy.moving:
                if random.random() < 0.7:
                    direction = random.choice(["up", "down", "left", "right"])
                    if direction == "up":
                        enemy.start_move_up()
                    elif direction == "down":
                        enemy.start_move_down()
                    elif direction == "left":
                        enemy.start_move_left()
                    elif direction == "right":
                        enemy.start_move_right()

                    def stop_enemy():
                        if enemy in self.enemies:
                            enemy.stop_move_up()
                            enemy.stop_move_down()
                            enemy.stop_move_left()
                            enemy.stop_move_right()

                    self.canvas.after(random.randint(500, 1500), stop_enemy)
                else:
                    self.enemy_shoot(enemy)

            self.canvas.after(random.randint(800, 1500), ai_loop)

        ai_loop()

    def enemy_shoot(self, enemy):
        """Выстрел врага"""
        if not enemy or enemy not in self.enemies:
            return

        x, y = enemy.get_position()
        direction = enemy.get_direction()

        bullet = Bullet(self.canvas, x, y, direction, owner=enemy, speed=8)
        bullet.game_frame = self
        self.bullets.append(bullet)

    def victory(self):
        """Победа на уровне"""
        # очищаем врагов
        for enemy in self.enemies:
            enemy.destroy()
        self.enemies.clear()

        # сообщение
        self.canvas.create_text(
            300, 300,
            text="ПОБЕДА!",
            font=("Arial", 24),
            fill="green"
        )



def show_level_settings():
    MainMenu.pack_forget()
    level_selection_frame.pack(fill="both", expand=True)


def start_level(level_num):
    level_data = levels[level_num]
    level_selection_frame.pack_forget()

    global game_frame
    game_frame = GameFrame(root, level_num, level_data, back_to_level_selection)
    game_frame.pack(fill="both", expand=True)


def back_to_level_selection():
    if game_frame:
        game_frame.destroy()
    level_selection_frame.pack(fill="both", expand=True)


def show_main2():
    level_selection_frame.pack_forget()
    MainMenu.pack(fill="both", expand=True)


def create_window():

    root.title("ТАНКИ2026")
    root.resizable(False, False)
    root.attributes('-fullscreen', True)
    global MainMenu, level_selection_frame
    def close_window():
        root.destroy()

    #тут типа подгрузка картинок крутых сам рисовал
    button_img = tk.PhotoImage(file="frame/images/button.png")
    logo_img = tk.PhotoImage(file="frame/images/logo.png")
    bok_img = tk.PhotoImage(file="frame/images/bok.png")

    #крутое главное меню
    MainMenu = tk.Frame(root, bg="Black")

    left_bok = tk.Label(MainMenu, image=bok_img, bg="black")
    left_bok.place(x=0, y=0, anchor="nw")
    right_bok = tk.Label(MainMenu, image=bok_img, bg="black")
    right_bok.place(x=root.winfo_screenwidth(), y=0, anchor="ne")


    logo_label = tk.Label(MainMenu, image=logo_img, bg="black")
    logo_label.pack(pady=20)


    play_btn = tk.Button(MainMenu, image=button_img, text="Играть", font=("Arial", 15), compound="center",command=show_level_settings, relief="flat", borderwidth=0, bg="black", activebackground="black", activeforeground="white")
    play_btn.pack(pady=10)

    exit_btn = tk.Button(MainMenu, image=button_img, text="Выход", font=("Arial", 15), compound="center", command=close_window, relief="flat", borderwidth=0, bg="black", activebackground="black", activeforeground="white")
    exit_btn.pack(pady=10)


    MainMenu.pack(fill="both", expand=True)

    #меню выбора уровней
    level_selection_frame = tk.Frame(root, bg="Black")
    tk.Label(level_selection_frame, text="Выбор уровня", font=("Arial", 20), bg="black", fg="white").pack(pady=20)

    # кнопки уровней 1-5
    for i in range(1, 6):
        btn = tk.Button(
            level_selection_frame,
            text=f"Уровень {i}",
            font=("Arial", 12),
            command=lambda lvl=i: start_level(lvl),
            width=15,
            height=1
        )
        btn.pack(pady=5)
    tk.Button(level_selection_frame, text="Назад", command=show_main2).pack(pady=20)


    root.mainloop()


if __name__ == "__main__":
    create_window()