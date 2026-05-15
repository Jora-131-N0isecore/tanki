import tkinter as tk


def show_settings():
    MainMenu.pack_forget()
    settings_frame.pack(fill="both", expand=True)


def show_level_settings():
    MainMenu.pack_forget()
    level_selection_frame.pack(fill="both", expand=True)


def show_main():
    settings_frame.pack_forget()
    MainMenu.pack(fill="both", expand=True)

def show_main2():
    level_selection_frame.pack_forget()
    MainMenu.pack(fill="both", expand=True)


def create_window():

    root = tk.Tk()
    root.geometry("800x800")
    root.title("ТАНКИ2026")
    root.resizable(False, False)
    root.attributes('-fullscreen', True)
    global MainMenu, settings_frame, level_selection_frame
    def close_window():
        root.destroy()

    #крутое главное меню
    MainMenu = tk.Frame(root)

    tk.Label(MainMenu, text="ГЛАВНОЕ МЕНЮ", font=("Arial", 20)).pack(pady=20)
    tk.Button(MainMenu, text="Играть", font=("Arial", 10), command=show_level_settings).pack(pady=10)
    tk.Button(MainMenu, text="Настройки", font=("Arial", 10), command=show_settings).pack(pady=10)
    tk.Button(MainMenu, text="Выход", font=("Arial", 10), command=close_window).pack(pady=10)
    MainMenu.pack(fill="both", expand=True)


    #тут меню настроек
    settings_frame = tk.Frame(root)
    tk.Label(settings_frame, text="Настройки", font=("Arial", 20)).pack(pady=20)
    tk.Button(settings_frame, text="Назад", command=show_main).pack(pady=10)
    tk.Button(settings_frame, text="Пустая кнопка").pack(pady=10)

    #меню выбора уровней
    level_selection_frame = tk.Frame(root)
    tk.Label(level_selection_frame, text="Выбор уровня", font=("Arial", 20)).pack(pady=20)
    tk.Button(level_selection_frame, text="Назад", command=show_main2).pack(pady=20)

    root.mainloop()


if __name__ == "__main__":
    create_window()