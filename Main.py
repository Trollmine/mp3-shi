# Mp3 reader V4:
import customtkinter
from tkinter import filedialog
from mutagen.mp3 import MP3
import pygame
import random
import os

app = customtkinter.CTk()
app.title("MP3-SHI")
app.geometry("500x400")

filesDirectory = "" #r"E:\PythonProject\mp3-shi\Songs"
filesList      = []
songsCount     = 0
playingSong    = "None"

musicTitle = customtkinter.CTkLabel(app, text="None")
musicTitle.pack(padx=20, pady=20)

playButton = customtkinter.CTkButton(app, text="PLAY")
playButton.pack(padx=20, pady=20)

changeDirectoryButton = customtkinter.CTkButton(app, text="SELECT DIRECTORY")
changeDirectoryButton.pack(padx=20, pady=20)

slider_volume = customtkinter.CTkSlider(app, from_=0, to=1, command=pygame.mixer.music.set_volume)
slider_volume.pack(padx=20, pady=20)

slider_time = customtkinter.CTkSlider(app, from_=0, to=1, command=pygame.mixer.music.set_pos, state="disabled")
slider_time.set(0)
slider_time.pack(padx=20, pady=20)


info_label = customtkinter.CTkLabel(app, text="", fg_color="transparent")
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

    pygame.mixer.music.load(os.path.join(filesDirectory, filesList[0]))
    songsCount = len(filesList)

    print(songsCount, filesList)

def play_music():
    global playingSong
    if playButton.cget("text") == "PAUSE":
        pygame.mixer.music.pause()
        playButton.configure(text="PLAY")

    elif playButton.cget("text") == "PLAY" and songsCount > 1:
        if playingSong != "None":
            pygame.mixer.music.unpause()

        else:
            pygame.mixer.music.play()
            playingSong = 0
            slider_time.set(0)
            slider_time.configure(to=MP3(os.path.join(filesDirectory, filesList[playingSong])).info.length, state="normal")
            musicTitle.configure(text=filesList[playingSong])

        info_label.configure(text="")
        playButton.configure(text="PAUSE")
    else:
        info_label.configure(text="You have no sound in the selected folder")

playButton.configure(command=play_music)
changeDirectoryButton.configure(command=choose_directory)

app.mainloop()
