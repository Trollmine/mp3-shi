# Mp3 reader V3:
import customtkinter
from tkinter import filedialog
import pygame
import random
import os

app = customtkinter.CTk()
app.geometry("500*400")

filesDirectory = "" #r"E:\PythonProject\mp3-shi\Songs"
filesList      = []
songsCount     = 0

playButton = customtkinter.CTkButton(app, text="PLAY")
playButton.pack(padx=20, pady=20)

changeDirectoryButton = customtkinter.CTkButton(app, text="SELECT DIRECTORY")
changeDirectoryButton.pack(padx=20, pady=20)

slider_volume = customtkinter.CTkSlider(app, from_=0, to=1, command=pygame.mixer.music.set_volume, orientation="vertical")
slider_volume.pack(padx=20, pady=20)

info_label=customtkinter.CTkLabel(app, text="", fg_color="transparent")
info_label.pack(padx=20, pady=20)

pygame.mixer.init()

def choose_directory():
    global filesDirectory
    global filesList
    global songsCount

    filesDirectory = filedialog.askdirectory(
        title="Choose your songs folder"
    )

    secondFilesList = os.listdir(filesDirectory)
    filesList = []
    print(secondFilesList)
    for file in secondFilesList:
        print(file)
        if file.lower().endswith((".mp3", ".wav", ".ogg")):
            filesList += [file]

    songsCount = len(filesList)

    print(songsCount, filesList)

def play_music():
    if playButton.cget("text") == "STOP":
        pygame.mixer.music.stop()
        playButton.configure(text="PLAY")

    elif playButton.cget("text") == "PLAY" and songsCount > 1:
        pygame.mixer.music.load(os.path.join(filesDirectory, filesList[random.randint(0, songsCount - 1)]))
        pygame.mixer.music.play()
        info_label.configure(text="")
        playButton.configure(text="STOP")
    else:
        info_label.configure(text="You have no sound in the selected folder")

playButton.configure(command=play_music)
changeDirectoryButton.configure(command=choose_directory)

app.mainloop()
