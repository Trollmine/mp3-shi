nter import filedialog
from PIL import ImageTk, Image
from mutagen.mp3 import MP3
import pygame
import random
import os
import time
import configparser

config = configparser.ConfigParser()

configPath    = os.path.join("Dependencies", "config.ini")
imagesPath    = os.path.join("Dependencies", "Images")
loopIconsPath = os.path.join(imagesPath, "LoopIcon")

loopIconsList = {
    0 : "noLoopIcon.png",
    1 : "loopOneIcon.png",
    2 : "loopAllIcon.png",
    3 : "loopAllRandomIcon.png",
}

customtkinter.set_appearance_mode("dark")

mainText_Color       = ("#000000", "#ffffff")
mainBackground_Color = ("#ffffff", "#4a536b")
foreground_Color     = ("#ff9a8d", "#40485d")
clickable_Color      = ()

app = customtkinter.CTk(fg_color=mainBackground_Color)
app.title("MP3-SHI")
app.geometry("960x540")
app.minsize(340, 540)
app.toplevel_window = None

filesDirectory = ""
filesList      = []
songsCount     = 0
playingSong    = -1   # -1 means there is no playing songs, otherwise the playingSong variable is the index of the playing song in the filesList list
loopMode       = 0    # 0= doesn't loop, 1= loop the same song, 2= loop all songs, 3= loop all songs randomly,
paused         = True

timePlayed = 0
lastPlayed = 0

app.grid_columnconfigure(0, weight=1)
app.grid_rowconfigure(1, weight=1)

musicTitle = customtkinter.CTkLabel(app, text="None", font=("", 30), text_color=mainText_Color)
musicTitle.grid(row=0, padx=20, pady=20, sticky="ewn")

topFrame = customtkinter.CTkFrame(app, fg_color=foreground_Color)
topFrame.grid(row=1, padx=20, pady=20, sticky="ewn")

topFrame.grid_columnconfigure(0, weight=1)
topFrame.grid_rowconfigure(1, weight=1)

slider_time = customtkinter.CTkSlider(topFrame, from_=0, to=1, state="disabled")
slider_time.set(0)
slider_time.grid(row=0, padx=20, pady=20, sticky="ew")

labelTime = customtkinter.CTkLabel(topFrame, fg_color=mainText_Color)

playFrame = customtkinter.CTkFrame(topFrame, fg_color=foreground_Color)
playFrame.grid(row=1, padx= 20, pady= 10, sticky="ewns")

playFrame.grid_columnconfigure(1, weight=1)

previousButton = customtkinter.CTkButton(playFrame, text="<", width=75, height=75, text_color=mainText_Color)
previousButton.grid(row=1, column=0, padx=5, pady=10, sticky="w")

playButton = customtkinter.CTkButton(playFrame, text="PLAY", width=75, height=75, text_color=mainText_Color)
playButton.grid(row=1, column=1, padx=5, pady=10, sticky="ew")

nextButton = customtkinter.CTkButton(playFrame, text=">", width=75, height=75, text_color=mainText_Color)
nextButton.grid(row=1, column=2, padx=5, pady=10, sticky="ew")

loopImage = customtkinter.CTkImage(Image.open(os.path.join(loopIconsPath, loopIconsList[loopMode])), Image.open(os.path.join(loopIconsPath, loopIconsList[loopMode])), (50,50))

loopButton = customtkinter.CTkButton(playFrame, image=loopImage, text="", width=75, height=75, text_color=mainText_Color)
loopButton.grid(row=1, column=3, padx=5, pady=10, sticky="e")

openSettingsButton = customtkinter.CTkButton(app, text="SETTINGS")
openSettingsButton.grid(padx=10, pady=10)

slider_volume = customtkinter.CTkSlider(app, from_=0, to=1, command=pygame.mixer.music.set_volume)
slider_volume.set(1)
slider_volume.grid(padx=20, pady=20)

info_label = customtkinter.CTkLabel(app, text="", fg_color="transparent")
info_label.grid(padx=20, pady=20)

pygame.mixer.init()

config.read(configPath)
if config.get('path_directory', 'path') == "none" or not config.get('path_directory', 'path'):
    info_label.configure(text="No songs folder selected, select one in the settings menu")
else:
    filesDirectory = config.get('path_directory', 'path')
    filesList      = os.listdir(filesDirectory)
    songsCount     = len(filesList)
    pygame.mixer.music.load(os.path.join(filesDirectory, filesList[0]))
    info_label.configure(text="your songs folder is " + config.get('path_directory', 'path') + " and you have " + str(songsCount) + " songs in this folder")

if config.get('QOL', 'loop_mode') != 0:
    loopMode = int(config.get('QOL', 'loop_mode'))
    loopImage.configure(light_image=Image.open(os.path.join(loopIconsPath, loopIconsList[loopMode])), dark_image=Image.open(os.path.join(loopIconsPath, loopIconsList[loopMode])))

def choose_directory():
    global filesDirectory, filesList, songsCount

    filesDirectory = filedialog.askdirectory(
        title="Choose your songs folder"
    )
    config.read(configPath)
    config.set('path_directory', 'path', filesDirectory)
    with open(configPath, 'w') as configfile:
        config.write(configfile)

    if filesDirectory:
        secondFilesList = os.listdir(filesDirectory)
        filesList = []

        for file in secondFilesList:
            print(file)
            if file.lower().endswith((".mp3", ".wav", ".ogg")):
                filesList += [file]

        pygame.mixer.music.load(os.path.join(filesDirectory, filesList[0]))
        songsCount = len(filesList)
        info_label.configure(
            text="your songs folder is " + config.get('path_directory', 'path') + " and you have " + str(
                songsCount) + " songs in this folder")

        print(songsCount, filesList)

def refresh_timePlayed(elapsedTime, isSlider):
    global timePlayed, lastPlayed

    if lastPlayed != 0:
        if isSlider:
            timePlayed = int(elapsedTime * 1000)
            lastPlayed = time.time() * 1000
        else:
            timePlayed += int(time.time() * 1000 - lastPlayed)
            lastPlayed = time.time() * 1000

    slider_time.set(timePlayed/1000)

def change_loop_mode():
    global loopMode

    if loopMode == 3:
        loopMode = 0
    else:
        loopMode += 1
    loopImage.configure(light_image=Image.open(os.path.join(loopIconsPath, loopIconsList[loopMode])), dark_image=Image.open(os.path.join(loopIconsPath, loopIconsList[loopMode])))
    config.set('QOL', 'loop_mode', str(loopMode))
    with open(configPath, 'w') as configfile:
        config.write(configfile)

def init_music():
    pygame.mixer.music.load(os.path.join(filesDirectory, filesList[playingSong]))
    pygame.mixer.music.play()
    slider_time.set(0)
    slider_time.configure(to=MP3(os.path.join(filesDirectory, filesList[playingSong])).info.length, state="normal")
    musicTitle.configure(text=("[", playingSong, "]", filesList[playingSong]))

def play_music():
    global playingSong, lastPlayed, paused
    if not paused:
        pygame.mixer.music.pause()
        playButton.configure(text="PLAY")
        paused = True
        refresh_timePlayed(0, False)

    elif paused and songsCount > 1:
        if playingSong != -1:
            pygame.mixer.music.unpause()
        else:
            playingSong = 0
            init_music()

        lastPlayed = time.time()*1000
        info_label.configure(text="")
        playButton.configure(text="PAUSE")
        paused = False
    else:
        info_label.configure(text="You have no sound in the selected folder")

def next_music():
    global playingSong,timePlayed ,paused
    if songsCount > 1:
        if songsCount-1 > playingSong:
            playingSong += 1
        elif songsCount-1 == playingSong:
            playingSong = 0

        init_music()

    playButton.configure(text="PAUSE")
    paused = False

    timePlayed = 0

def prev_music():
    global playingSong, timePlayed, paused
    if songsCount > 1:
        if playingSong > 0:
            playingSong -= 1
        elif playingSong == 0:
            playingSong = songsCount - 1

        init_music()

    playButton.configure(text="PAUSE")
    paused = False

    timePlayed = 0

Windows = []
def open_window(Name):
    global Windows
    for i in Windows:
        i.destroy()

    NewWindow = customtkinter.CTkToplevel(app, fg_color=mainBackground_Color)
    NewWindow.title(Name)
    NewWindow.geometry("300x300")
    if Name == "Settings":
        NewWindow.resizable(False, False)
        changeDirectoryButton = customtkinter.CTkButton(master=NewWindow, text="SELECT DIRECTORY", command=choose_directory)
        changeDirectoryButton.grid(padx=20, pady=20)
    Windows.insert(len(Windows),NewWindow)

playButton.configure(command=play_music)

openSettingsButton.configure(command=lambda: open_window("Settings"))

nextButton.configure(command=next_music)
previousButton.configure(command=prev_music)

loopButton.configure(command=change_loop_mode)

slider_time.configure(command=lambda x: [pygame.mixer.music.set_pos(slider_time.get()), refresh_timePlayed(slider_time.get(), True)])

def refresh_thread():
    global paused, playingSong, timePlayed
    while True:
        if pygame.mixer.music.get_busy():
            refresh_timePlayed(-1, False)
        elif not paused:
            print("finished")
            pygame.mixer.music.unload()
            if loopMode == 0:
                pygame.mixer.music.load(os.path.join(filesDirectory, filesList[playingSong]))
                slider_time.configure(to=MP3(os.path.join(filesDirectory, filesList[playingSong])).info.length,state="normal")
                pygame.mixer.music.play()
                pygame.mixer.music.pause()
                playButton.configure(text="PLAY")
                slider_time.set(0)
                timePlayed = 0
                paused = True
            elif loopMode == 1:
                init_music()
                playButton.configure(text="PAUSE")
                timePlayed = 0
                paused = False
            elif loopMode == 2:
                if songsCount > 1:
                    next_music()
                    playButton.configure(text="PAUSE")
                    timePlayed = 0
                    paused = False
                else:
                    init_music()
                    playButton.configure(text="PAUSE")
                    timePlayed = 0
                    paused = False
            elif loopMode == 3:
                if songsCount > 1:
                    randNum = random.randint(0,len(filesList)-1)
                    while randNum == playingSong:
                        randNum = random.randint(0,len(filesList)-1)
                    playingSong = randNum
                    init_music()
                    playButton.configure(text="PAUSE")
                    timePlayed = 0
                    paused = False
                else:
                    init_music()
                    playButton.configure(text="PAUSE")
                    timePlayed = 0
                    paused = False

        time.sleep(.05)
refreshThread = threading.Thread(target=refresh_thread)
refreshThread.start()

app.mainloop()

os._exit(0) # Stops the script from running after the main window's closed, preventing threads to keep on running after we close the app
