# Mp3 reader V2:
import customtkinter
from tkinter import filedialog
import pathlib
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

def choose_directory():
    global filesDirectory
    global filesList
    global songsCount

    filesDirectory = filedialog.askdirectory(
        title="Choose your songs folder"
    )
    filesList = os.listdir(filesDirectory)
    songsCount = 0
    for path in pathlib.Path(filesDirectory).iterdir():
        if path.is_file():
            songsCount += 1
    print(filesList)

def play_music():
    if playButton.cget("text") == "STOP":
        pygame.mixer.music.stop()
        playButton.configure(text="PLAY")
    else:
        pygame.mixer.init()
        pygame.mixer.music.load(os.path.join(filesDirectory, filesList[random.randint(0, songsCount-1)]))
        pygame.mixer.music.play()
        playButton.configure(text="STOP")

playButton.configure(command=play_music)

changeDirectoryButton = customtkinter.CTkButton(app, text="SELECT DIRECTORY", command=choose_directory)
changeDirectoryButton.pack(padx=20, pady=20)

app.mainloop()
