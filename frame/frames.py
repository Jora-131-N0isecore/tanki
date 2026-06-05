import tkinter as tk
from .tank import Tank


root = tk.Tk()

"""
тут типа крч да словарь так называемый с данными об уровнях пока пустышка потом сделаю
интересно это ктото кроме меня будет читать
"""
levels = {
    1: {"bricks": [],
         "steel": [(2,2), (3,2), (4,2), (5,2), (6,2),  # стена из стали
                  (2,12), (3,12), (4,12), (5,12), (6,12)], "eagle": (10, 10)},
    2: {"bricks": [], "steel": [
        (1,1), (2,2)
    ], "eagle": (10, 10)},
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
        self.cell_size = 40  # размер одной клетки в пикселях
        self.map_width = 15
        self.map_height = 15
        self.steel_texture = None

        self.create_widgets()
        self.load_textures()
        self.create_map()

    def create_widgets(self):
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

    def create_map(self):
        # временная сетка чтобы откладка была удобнеэ
        for row in range(self.map_height):
            for col in range(self.map_width):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                # временно просто клетки с границами
                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    outline="gray",
                    fill="darkgreen"
                )

        # TODO: позже добавлю тут отрисовку кирпичей, стали и орла
        self.player_tank = Tank(self.canvas, 300, 300, tank_type="player", size=40)
        self.player_tank.map_width = self.map_width
        self.player_tank.map_height = self.map_height
        self.player_tank.steel_blocks = self.level_data.get("steel", [])

        for col, row in self.level_data.get("steel", []):
            x1 = col * self.cell_size
            y1 = row * self.cell_size
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size


            self.canvas.create_image(
                x1 + self.cell_size // 2,
                y1 + self.cell_size // 2,
                image=self.steel_texture,
                anchor="center"
                )

    def load_textures(self):
        self.steel_texture = tk.PhotoImage(file="frame/images/steel.png")


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