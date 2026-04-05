import tkinter as tk


def show_settings():
    MainMenu.pack_forget()
    settings_frame.pack(fill="both", expand=True)


def show_main():
    settings_frame.pack_forget()
    MainMenu.pack(fill="both", expand=True)

def create_window():

    root = tk.Tk()
    root.geometry("600x600")
    root.title("ТАНКИ2026")
    global MainMenu, settings_frame

    #крутое главное меню
    MainMenu = tk.Frame(root)
    tk.Label(MainMenu, text="ГЛАВНОЕ МЕНЮ", font=("Arial", 20)).pack(pady=20)
    tk.Button(MainMenu, text="Играть", font=("Arial", 10)).pack(pady=10)
    tk.Button(MainMenu, text="Настройки", font=("Arial", 10), command=show_settings).pack(pady=10)
    tk.Button(MainMenu, text="Выход", font=("Arial", 10)).pack(pady=10)
    MainMenu.pack(fill="both", expand=True)


    #тут меню настроек
    settings_frame = tk.Frame(root)
    tk.Label(settings_frame, text="Настройки", font=("Arial", 20)).pack(pady=20)
    tk.Button(settings_frame, text="Назад", command=show_main).pack(pady=10)
    tk.Button(settings_frame, text="Пустая кнопка").pack(pady=10)


    root.mainloop()

if __name__ == "__main__":
    create_window()