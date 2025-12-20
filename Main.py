# Mp3 reader V2:
from turtle import right
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
pygame.mixer.init()

def choose_directory():
    global filesDirectory
    global filesList
    global songsCount

    filesDirectory = filedialog.askdirectory(
        title="Choose your songs folder"
    )
    filesList = [
    f for f in os.listdir(filesDirectory)
    if f.lower().endswith((".mp3", ".wav", ".ogg"))]

    songsCount = len(filesList)
    
    print(songsCount,filesList)

def play_music():
    if playButton.cget("text") == "STOP":
        pygame.mixer.music.stop()
        playButton.configure(text="PLAY")
    elif playButton.cget("text") != "STOP" and songsCount>1 :
        pygame.mixer.music.load(os.path.join(filesDirectory, filesList[random.randint(0, songsCount-1)]))
        pygame.mixer.music.play()
        info_label.configure(text="")
        playButton.configure(text="STOP")
    elif songsCount==0:
        info_label.configure(text="You have no sound in the selected folder")




info_label=customtkinter.CTkLabel(app, text="", fg_color="transparent")
info_label.pack(pady=20)

playButton = customtkinter.CTkButton(app, text="PLAY")
playButton.pack(padx=20, pady=20)
playButton.configure(command=play_music)


changeDirectoryButton = customtkinter.CTkButton(app, text="SELECT DIRECTORY", command=choose_directory)
changeDirectoryButton.pack(padx=20, pady=20)


slider_volume = customtkinter.CTkSlider(app, 
from_=0.0, 
to=1.0, 
command=pygame.mixer.music.set_volume,
orientation="vertical"
)
slider_volume.pack(pady=20,)


app.mainloop()
