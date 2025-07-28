from tkinter import *
import tkinter as tk
import json
from PIL import Image, ImageTk
import subprocess
import os


# function

def play_game(emulator, rom):
    if emulator:
        if os.path.exists(emulator) and os.path.exists(rom):
            subprocess.Popen([emulator, rom])
        else:
            print("Emulator or Rom not found")

    else:
        if os.path.exists(rom):
            subprocess.Popen(rom)
        else:
            print("Game not found")


def Game_page(game):
    root.destroy()
    page_game = tk.Tk()
    page_game.geometry("1440x800")
    page_game.title(game['name'])


    # Cover Image
    images = Image.open(game['cover']).resize((300, 250))
    cover_image = ImageTk.PhotoImage(images)
    label = tk.Label(page_game, image=cover_image)
    label.image = cover_image
    label.grid(row=1, column=0, padx=50, pady=50)

    # Play Button
    original_image = Image.open("Image/17762.png")
    resized_image = original_image.resize((32, 32), Image.LANCZOS)
    play_icon = ImageTk.PhotoImage(resized_image)

    button = Button(page_game, text="Play",
                    font=("Arial", 20),
                    image=play_icon,
                    compound="left",
                    command=lambda: play_game(game['emulator'], game['rom']),
                    width=150, height=50,
                    bg="#52FA0F"
                    )
    button.image = play_icon  # fix typo: button.imgae → button.image
    button.grid(row=1, column=1)

    # Description
    description_label = tk.Label(page_game,
                                 text=game["description"],
                                 wraplength=400,
                                 justify="left",
                                 font=("Arial", 12),
                                 fg="gray"
                                 )
    description_label.grid(row=2, column=0, padx=10, pady=10)

    if 'screenshots' in game and isinstance(game['screenshots'], list):
        max_per_row = 3
        for i, shot in enumerate(game['screenshots']):
            if os.path.exists(shot):
                shot_img = Image.open(shot).resize((200, 180))  # Resize
                shot_img_tk = ImageTk.PhotoImage(shot_img)

                row = 6 + (i // max_per_row)
                col = i % max_per_row

                shot_label = tk.Label(page_game, image=shot_img_tk)
                shot_label.image = shot_img_tk  # prevent garbage collection
                shot_label.grid(row=row, column=col, padx=5, pady=5)

   
    label.image =cover_image
    

def create_game_grid(games):
    rows = (len(games) // 6) + 1
    for index, game in enumerate(games):
        row = index // 6
        col = index % 6

        img = Image.open(game['cover']).resize((200, 200))
        cover_img = ImageTk.PhotoImage(img)

        btn = tk.Button(root, image=cover_img, command=lambda g=game: Game_page(g))
        btn.grid(row=row, column=col, padx=10, pady=10)        
        btn.image = cover_img 

def load_data():
    with open("games.json", "r", encoding="utf-8") as files:
        return json.load(files)


global root
root = tk.Tk()
root.title("Game Lists")
root.geometry("1440x800")

# JSON Data covers
games = load_data()
create_game_grid(games)

root.mainloop()