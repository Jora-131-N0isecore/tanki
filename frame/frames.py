import tkinter as tk


def show_level_settings():
    MainMenu.pack_forget()
    level_selection_frame.pack(fill="both", expand=True)


def show_main2():
    level_selection_frame.pack_forget()
    MainMenu.pack(fill="both", expand=True)


def create_window():

    root = tk.Tk()
    root.geometry("800x800")
    root.title("ТАНКИ2026")
    root.resizable(False, False)
    root.attributes('-fullscreen', True)
    global MainMenu, level_selection_frame
    def close_window():
        root.destroy()

    #тут типа подгрузка картинок крутых сам рисовал
    button_img = tk.PhotoImage(file="images/button.png")
    logo_img = tk.PhotoImage(file="images/logo.png")
    bok_img = tk.PhotoImage(file="images/bok.png")

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
    level_selection_frame = tk.Frame(root)
    tk.Label(level_selection_frame, text="Выбор уровня", font=("Arial", 20)).pack(pady=20)
    tk.Button(level_selection_frame, text="Назад", command=show_main2).pack(pady=20)

    root.mainloop()


if __name__ == "__main__":
    create_window()