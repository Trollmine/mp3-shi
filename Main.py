# Mp3 reader V6:
import customtkinter
from tkinter import filedialog
from mutagen.mp3 import MP3
import pygame
import random
import os

from sqlalchemy import column

app = customtkinter.CTk(fg_color="#ff8838")
app.title("MP3-SHI")
app.geometry("960x540")

filesDirectory = "" #r"E:\PythonProject\mp3-shi\Songs"
filesList      = []
songsCount     = 0
playingSong    = -1

musicTitle = customtkinter.CTkLabel(app, text="None", font=("", 30))
musicTitle.pack(padx=20, pady=20)

topFrame = customtkinter.CTkFrame(app, width=960, height=540, fg_color="#fa9857")
topFrame.pack(padx=20, pady=20)

sliderFrame = customtkinter.CTkFrame(topFrame, fg_color="#fa9857")
sliderFrame.grid(row=0, column=1, sticky="ew")

previousButton = customtkinter.CTkButton(topFrame, text="<", width=50, height=50)
previousButton.grid(row=1, column=0, padx=10, pady=20)

playButton = customtkinter.CTkButton(topFrame, text="PLAY", width=50, height=50)
playButton.grid(row=1, column=1, padx=0, pady=20, sticky="ew")

nextButton = customtkinter.CTkButton(topFrame, text=">", width=50, height=50)
nextButton.grid(row=1, column=2, padx=10, pady=20)

slider_time = customtkinter.CTkSlider(sliderFrame, from_=0, to=1, command=pygame.mixer.music.set_pos, state="disabled")
slider_time.set(0)
slider_time.grid(padx=20, pady=20)

changeDirectoryButton = customtkinter.CTkButton(app, text="SELECT DIRECTORY")
changeDirectoryButton.pack(padx=20, pady=20)

slider_volume = customtkinter.CTkSlider(app, from_=0, to=1, command=pygame.mixer.music.set_volume)
slider_volume.set(1)
slider_volume.pack(padx=20, pady=20)

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
        if playingSong != -1:
            pygame.mixer.music.unpause()

        else:
            pygame.mixer.music.play()
            playingSong = 0
            slider_time.set(0)
            slider_time.configure(to=MP3(os.path.join(filesDirectory, filesList[playingSong])).info.length, state="normal")
            musicTitle.configure(text=("[", playingSong, "]", filesList[playingSong]))

        info_label.configure(text="")
        playButton.configure(text="PAUSE")
    else:
        info_label.configure(text="You have no sound in the selected folder")

def next_music():
    global playingSong
    if songsCount > 1:
        if songsCount-1 > playingSong:
            playingSong += 1
        elif songsCount-1 == playingSong:
            playingSong = 0
        pygame.mixer.music.load(os.path.join(filesDirectory, filesList[playingSong]))
        pygame.mixer.music.play()
        musicTitle.configure(text=("[", playingSong , "]", filesList[playingSong]))

def prev_music():
    global playingSong
    if songsCount > 1:
        if playingSong > 0:
            playingSong -= 1
        elif playingSong == 0:
            playingSong = songsCount - 1
        pygame.mixer.music.load(os.path.join(filesDirectory, filesList[playingSong]))
        pygame.mixer.music.play()
        musicTitle.configure(text=("[", playingSong , "]", filesList[playingSong]))

playButton.configure(command=play_music)
changeDirectoryButton.configure(command=choose_directory)

nextButton.configure(command=next_music)
previousButton.configure(command=prev_music)

app.mainloop()
