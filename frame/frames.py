import tkinter as tk
from .tank import Tank
from .bullet import Bullet
from .score_system import ScoreSystem
import random


root = tk.Tk()

levels = {
    1: {
        "bricks": [
            (5,5), (5,6), (5,7), (5,8),
            (6,5), (6,6), (6,7), (6,8),
            (7,5), (7,6),
            (8,5), (8,6), (8,7), (8,8)
        ],
        "steel": [
            (2,2), (3,2), (4,2), (5,2), (6,2), (7,2), (8,2), (9,2), (10,2), (11,2), (12,2),
            (2,12), (3,12), (4,12), (5,12), (6,12), (7,12), (8,12), (9,12), (10,12), (11,12), (12,12)
        ],
        "eagle": (7, 13),
        "enemies_total": 10
    },
    2: {
        "bricks": [
            (3,3), (3,4), (3,5), (3,6), (3,7), (3,8), (3,9), (3,10),
            (11,3), (11,4), (11,5), (11,6), (11,7), (11,8), (11,9), (11,10)
        ],
        "steel": [
            (1,1), (2,1), (12,1), (13,1),
            (1,13), (2,13), (12,13), (13,13)
        ],
        "eagle": (7, 13),
        "enemies_total": 15
    },
    3: {
        "bricks": [
            (2,2), (2,3), (2,4), (2,5), (2,6), (2,7), (2,8), (2,9), (2,10), (2,11),
            (12,2), (12,3), (12,4), (12,5), (12,6), (12,7), (12,8), (12,9), (12,10), (12,11)
        ],
        "steel": [
            (5,2), (6,2), (7,2), (8,2), (9,2),
            (5,12), (6,12), (7,12), (8,12), (9,12)
        ],
        "eagle": (7, 13),
        "enemies_total": 20
    },
    4: {
        "bricks": [
            (1,2), (2,2), (3,2), (4,2),
            (1,3), (2,3), (3,3), (4,3),
            (10,2), (11,2), (12,2), (13,2),
            (10,3), (11,3), (12,3), (13,3)
        ],
        "steel": [
            (3,5), (4,5), (5,5), (6,5), (7,5), (8,5), (9,5), (10,5), (11,5),
            (3,9), (4,9), (5,9), (6,9), (7,9), (8,9), (9,9), (10,9), (11,9)
        ],
        "eagle": (7, 13),
        "enemies_total": 20
    },
    5: {
        "bricks": [
            (2,2), (2,3), (2,4), (3,2), (3,3), (3,4), (4,2), (4,3), (4,4),
            (10,2), (10,3), (10,4), (11,2), (11,3), (11,4), (12,2), (12,3), (12,4),
            (2,10), (2,11), (2,12), (3,10), (3,11), (3,12), (4,10), (4,11), (4,12),
            (10,10), (10,11), (10,12), (11,10), (11,11), (11,12), (12,10), (12,11), (12,12)
        ],
        "steel": [
            (5,1), (6,1), (7,1), (8,1), (9,1),
            (5,2), (9,2),
            (5,13), (6,13), (7,13), (8,13), (9,13),
            (5,12), (9,12)
        ],
        "eagle": (7, 13),
        "enemies_total": 25
    }
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


        self.brick_blocks = []
        self.steel_blocks = []
        self.bullets = []

        # настройки стрельбы
        self.can_shoot = True
        self.shoot_delay = 1000

        # текстуры
        self.steel_texture = None
        self.brick_texture = None
        self.eagle_texture = None
        self.eagle_position = None
        self.eagle_id = None

        self.lives = 3

        self.score_system = ScoreSystem()
        self.score_system.set_level(level_num)

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
        self.score_label = tk.Label(top_frame, text=f"Очки: 0",
                                    font=("Arial", 14), bg="black", fg="yellow")
        self.score_label.pack(side="left", padx=20)

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
        eagle_pos = self.level_data.get("eagle")
        if eagle_pos:
            col, row = eagle_pos
            self.eagle_position = (col, row)
            x1 = col * self.cell_size
            y1 = row * self.cell_size
            self.eagle_id = self.canvas.create_image(
                x1 + self.cell_size // 2,
                y1 + self.cell_size // 2,
                image=self.eagle_texture,
                anchor="center",
                tags=("eagle",)
            )
        self.start_enemy_spawn()


    def load_textures(self):
        self.eagle_texture = tk.PhotoImage(file="frame/images/eagle.png")
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
        #Возрождает танк игрока после потери жизни
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



        # защита на 1 секунду после респавна
        self.invincible_frames = 60
        self.canvas.after(16, self.update_invincibility)

    def update_lives_display(self):
        #Обновляет отображение жизней на панели
        if hasattr(self, 'lives_label'):
            self.lives_label.config(text=f"Жизни: {self.lives}")

    def update_invincibility(self):
        #Обновляет состояние неуязвимости
        if hasattr(self, 'invincible_frames') and self.invincible_frames > 0:
            self.invincible_frames -= 1

    def lose_life(self):
        #Потеря одной жизни
        self.lives -= 1
        self.score_system.add_points(-250)
        self.update_score_display()
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
        self.enemies_total = 0
        self.enemies_killed = 0
        self.enemies_spawned = 100
        #Конец игры
        if hasattr(self, 'player_tank') and self.player_tank:
            self.player_tank.destroy()

        for enemy in self.enemies:
            enemy.destroy()
        self.enemies.clear()

        for bullet in self.bullets:
            bullet.destroy()
        self.bullets.clear()

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
        update_level_records()

    def eagle_destroyed(self):
        #Орёл уничтожен
        # останавливаем спавн врагов
        self.enemies_total = 0
        self.enemies_killed = 0
        self.enemies_spawned = 100

        # удаляем орла
        if self.eagle_id:
            self.canvas.delete(self.eagle_id)
            self.eagle_id = None

        # удаляем игрока
        if hasattr(self, 'player_tank') and self.player_tank:
            self.player_tank.destroy()

        # удаляем всех врагов
        for enemy in self.enemies[:]:
            enemy.destroy()
        self.enemies.clear()

        # удаляем все пули
        for bullet in self.bullets[:]:
            bullet.destroy()
        self.bullets.clear()

        # сообщение о поражении
        self.canvas.create_text(
            300, 300,
            text="ОРЁЛ УНИЧТОЖЕН!\nИГРА ОКОНЧЕНА",
            font=("Arial", 24),
            fill="red"
        )
        update_level_records()

    def start_enemy_spawn(self):
        #Запускает спавн врагов
        self.spawn_enemy()
        if self.enemies_killed < self.enemies_total:
            self.canvas.after(3000, self.start_enemy_spawn)

    def spawn_enemy(self):
        #Создаёт одного врага
        if self.enemies_killed >= self.enemies_total:
            return
        if self.enemies_spawned >= self.enemies_total:
            return
        if len(self.enemies) >= self.max_enemies:
            return


        x, y = random.choice(self.spawn_positions)

        enemy = Tank(self.canvas, x, y, tank_type="enemy", size=40, speed=2)
        enemy.game_frame = self
        enemy.direction = "down"
        enemy.draw()

        self.enemies.append(enemy)
        self.start_enemy_ai(enemy)

        self.enemies_spawned += 1

    def start_enemy_ai(self, enemy):
        #ИИ врага


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
        #Выстрел врага
        if not enemy or enemy not in self.enemies:
            return

        x, y = enemy.get_position()
        direction = enemy.get_direction()

        bullet = Bullet(self.canvas, x, y, direction, owner=enemy, speed=8)
        bullet.game_frame = self
        self.bullets.append(bullet)

    def victory(self):
        #Победа на уровне
        self.score_system.check_and_save_record()
        update_level_records()
        # очищаем врагов
        for enemy in self.enemies:
            enemy.destroy()
        self.enemies.clear()



        if hasattr(self, 'player_tank') and self.player_tank:
            self.player_tank.destroy()

        # сообщение
        self.canvas.create_text(
            300, 300,
            text="ПОБЕДА!",
            font=("Arial", 24),
            fill="green"
        )

    def update_score_display(self):
        if hasattr(self, 'score_label'):
            self.score_label.config(text=f"Очки: {self.score_system.get_current_score()}")





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
def update_level_records():
    #Обновляет текст на кнопках уровней с новыми рекордами
    temp_score = ScoreSystem()
    for i, btn in enumerate(level_buttons, 1):
        record = temp_score.get_record_for_level(i)
        btn.config(text=f"Уровень {i} (рекорд: {record})")

def create_window():

    root.title("ТАНКИ2026")
    root.resizable(False, False)
    root.attributes('-fullscreen', True)
    global MainMenu, level_selection_frame
    def close_window():
        root.destroy()

    #тут подгрузка картинок
    button_img = tk.PhotoImage(file="frame/images/button.png")
    logo_img = tk.PhotoImage(file="frame/images/logo.png")
    bok_img = tk.PhotoImage(file="frame/images/bok.png")

    #главное меню
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
    temp_score = ScoreSystem()
    global level_buttons
    level_buttons = []  # список для хранения кнопок

    for i in range(1, 6):
        record = temp_score.get_record_for_level(i)
        btn_text = f"Уровень {i} (рекорд: {record})"
        btn = tk.Button(
            level_selection_frame,
            text=btn_text,
            font=("Arial", 12),
            command=lambda lvl=i: start_level(lvl),
            width=20,
            height=1
        )
        btn.pack(pady=5)
        level_buttons.append(btn)
    tk.Button(level_selection_frame, text="Назад", command=show_main2).pack(pady=20)


    root.mainloop()


if __name__ == "__main__":
    create_window()