# Mp3-shi V15:
import threading

import customtkinter
from tkinter import filedialog
from PIL import Image
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

playlists = {
}

config.read(configPath)
for playlist in config["playlists"]:
    songslist = config["playlists"][playlist].split(",")
    del songslist[-1]
    playlists[playlist] = songslist

print(playlists)
"""
config.read(configPath)
for playlist in playlists:
    songs = ""
    for song in playlists[playlist]:
        songs += str(song) + ","
    print(playlist)
    config.set("playlists", playlist, songs)

with open(configPath, 'w') as configfile:
    config.write(configfile)
"""

loopIconsList = {
    0 : ["noLoopLight.png", "noLoopDark.png"],
    1 : ["loopOneLight.png", "loopOneDark.png"],
    2 : ["loopAllLight.png", "loopAllDark.png"],
    3 : ["loopRandomLight.png", "loopRandomDark.png"],
}

mainText_color       = ("#ffedd3", "#bdd0ff")
mainBackground_color = ("#ffd59a", "#4a536b")
foreground_color     = ("#ffc26c", "#40485d")
clickable_color      = ("#ffb246", "#3d538c")
main_hover_color     = ("#d99739", "#2a3c6c")
main_bars_color      = ("#ffdfb2", "#6a748e")
hover_bars_color     = ("#e3c7a1", "#4f5668")

unselected_color       = clickable_color
selected_color         = ("#7ee451", "#3d8c57")
unselected_text_color  = mainText_color
selected_text_color    = ("#e7ffdc", "#a5deb8")
unselected_hover_color = main_hover_color
selected_hover_color   = ("#4aa422", "#176e34")

app = customtkinter.CTk(fg_color=mainBackground_color)
app.title("MP3-SHI")
app.geometry("960x540")
app.minsize(540, 540)
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
#app.grid_rowconfigure(1, weight=1)

musicTitle = customtkinter.CTkLabel(app, text="", font=("", 50), text_color=mainText_color)
musicTitle.grid(row=0, padx=20, pady=20, sticky="ewn")

# topFrame part
topFrame = customtkinter.CTkFrame(app, fg_color=foreground_color)
topFrame.grid(row=2, padx=20, pady=20, sticky="ewn")
topFrame.grid_columnconfigure(0, weight=1)

# sliderFrame in topFrame part
sliderFrame = customtkinter.CTkFrame(topFrame, fg_color="transparent")
sliderFrame.grid(row=0, padx= 20, pady= 5, sticky="ew")
sliderFrame.grid_columnconfigure(1, weight=1)

timer_text  = customtkinter.CTkLabel(sliderFrame, width=10, height=20, text="00:00", text_color=mainText_color, font=("", 20))
timer_text.grid(row=0, column=0, padx=20, pady=20, sticky="ewn")

timer_end_text  = customtkinter.CTkLabel(sliderFrame, width=10, height=20, text="00:00", text_color=mainText_color, font=("", 20))
timer_end_text.grid(row=0, column=2, padx=20, pady=20, sticky="ewn")

slider_time = customtkinter.CTkSlider(sliderFrame, from_=0, to=1, state="disabled", button_color=clickable_color, button_hover_color=main_hover_color, progress_color=main_bars_color, fg_color=hover_bars_color)
slider_time.set(0)
slider_time.grid(row=0, column=1, padx=10, pady=20, sticky="ewn")

# TopFrame in topFrame part
very_topFrame = customtkinter.CTkFrame(topFrame, fg_color="transparent", height=50)
very_topFrame.grid(row=1, padx=20, pady=0)

openMusicButton = customtkinter.CTkButton(very_topFrame, text="CHOOSE A FILE", fg_color=clickable_color, hover_color=main_hover_color, text_color=mainText_color, width=100)
openMusicButton.grid(padx=10, pady=10, row=0, column=0, sticky="ew")

playlistButton = customtkinter.CTkButton(very_topFrame, text="PLAYLISTS", fg_color=clickable_color, hover_color=main_hover_color, text_color=mainText_color, width=100)
playlistButton.grid(padx=10, pady=10, row=0, column=1, sticky="ew")

openSettingsButton = customtkinter.CTkButton(very_topFrame, text="SETTINGS", fg_color=clickable_color, hover_color=main_hover_color, text_color=mainText_color, width=100)
openSettingsButton.grid(padx=10, pady=10, row=0, column=2, sticky="ew")

# playFrame in topFrame part
playFrame = customtkinter.CTkFrame(topFrame, fg_color=foreground_color)
playFrame.grid(row=2, padx= 20, pady= 5, sticky="ewns")
playFrame.grid_columnconfigure(1, weight=1)

previousButton = customtkinter.CTkButton(playFrame, text="<", width=75, height=75, text_color=mainText_color, fg_color=clickable_color, hover_color=main_hover_color, font=("", 60))
previousButton.grid(row=1, column=0, padx=5, pady=10, sticky="w")

playButton = customtkinter.CTkButton(playFrame, text="PLAY", width=75, height=75, text_color=mainText_color, fg_color=clickable_color, hover_color=main_hover_color, font=("", 40))
playButton.grid(row=1, column=1, padx=5, pady=10, sticky="ew")

nextButton = customtkinter.CTkButton(playFrame, text=">", width=75, height=75, text_color=mainText_color, fg_color=clickable_color, hover_color=main_hover_color, font=("", 60))
nextButton.grid(row=1, column=2, padx=5, pady=10, sticky="ew")

loopImage = customtkinter.CTkImage(light_image=Image.open(os.path.join(loopIconsPath, loopIconsList[loopMode][0])), dark_image=Image.open(os.path.join(loopIconsPath, loopIconsList[loopMode][1])), size=(50, 50))

loopButton = customtkinter.CTkButton(playFrame, image=loopImage, text="", width=75, height=75, text_color=mainText_color, fg_color=clickable_color, hover_color=main_hover_color)
loopButton.grid(row=1, column=3, padx=5, pady=10, sticky="e")

slider_volume = customtkinter.CTkSlider(app, from_=0, to=1, command=pygame.mixer.music.set_volume, button_color=clickable_color, button_hover_color=main_hover_color, progress_color=main_bars_color, fg_color=hover_bars_color)
slider_volume.set(1)
slider_volume.grid(padx=20, pady=20)

info_label = customtkinter.CTkLabel(app, text="", fg_color="transparent")
info_label.grid(padx=20, pady=20)

pygame.mixer.init()

config.read(configPath)
if config.get('path_directory', 'path') == "none" or not config.get('path_directory', 'path') or not os.path.exists(config.get('path_directory', 'path')) :
    info_label.configure(text="No songs folder selected, or not found, select one in the settings menu")
else:
    filesDirectory = config.get('path_directory', 'path')
    filesList      = os.listdir(filesDirectory)
    songsCount     = len(filesList)
    pygame.mixer.music.load(os.path.join(filesDirectory, filesList[0]))
    info_label.configure(text="your songs folder is " + config.get('path_directory', 'path') + " and you have " + str(songsCount) + " songs in this folder")

if int(config.get('QOL', 'loop_mode')) != 0:
    loopMode = int(config.get('QOL', 'loop_mode'))
    loopImage.configure(light_image=Image.open(os.path.join(loopIconsPath, loopIconsList[loopMode][0])), dark_image=Image.open(os.path.join(loopIconsPath, loopIconsList[loopMode][1])))

def change_color_mode():
    config.read(configPath)
    if customtkinter.get_appearance_mode() == "Light":
        customtkinter.set_appearance_mode("Dark")
        config.set('QOL', 'dark_mode', "enabled")
    else:
        customtkinter.set_appearance_mode("Light")
        config.set('QOL', 'dark_mode', "disabled")
    with open(configPath, 'w') as configfile:
        config.write(configfile)

if config.get('QOL', 'dark_mode') == "enabled":
    customtkinter.set_appearance_mode("dark")
else:
    customtkinter.set_appearance_mode("light")

def choose_song():
    if filesDirectory and songsCount > 0:
        open_window("CHOOSE A SONG")

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
            if file.lower().endswith((".mp3", ".wav", ".ogg")):
                filesList += [file]

        pygame.mixer.music.load(os.path.join(filesDirectory, filesList[0]))
        songsCount = len(filesList)
        info_label.configure(
            text="your songs folder is " + config.get('path_directory', 'path') + " and you have " + str(
                songsCount) + " songs in this folder")

new_playlist_songs_list = []
def create_playlist(button, name):
    global new_playlist_songs_list
    global playlists

    name = name.removesuffix("\n")

    playlists[name] = new_playlist_songs_list
    button.destroy()

    config.read(configPath)
    songs = ""
    for song in new_playlist_songs_list:
        print(song)
        songs += str(song) + ","
    print(songs)
    config.set("playlists", name, songs)

    with open(configPath, 'w') as configfile:
        config.write(configfile)
    print(playlists)
    
    new_playlist_songs_list = []

def select_songs_to_create_playlist():
    open_window("Create playlist")

    print("creating playlist")

def select_song(button, songnum):
    global new_playlist_songs_list
    if button.cget("fg_color") == unselected_color:
        button.configure(fg_color=selected_color, hover_color=selected_hover_color, text_color=selected_text_color)
        new_playlist_songs_list += [songnum]
    else:
        button.configure(fg_color=unselected_color, hover_color=unselected_hover_color, text_color=unselected_text_color)
        new_playlist_songs_list -= [songnum]

def refresh_timePlayed(elapsedTime, isSlider):
    global timePlayed, lastPlayed

    #print(elapsedTime, isSlider, timePlayed, lastPlayed)

    if lastPlayed != 0:
        if isSlider:
            timePlayed = int(elapsedTime * 1000)
            lastPlayed = time.time() * 1000
        else:
            timePlayed += int(time.time() * 1000 - lastPlayed)
            lastPlayed = time.time() * 1000
    else:
        lastPlayed = time.time() * 1000

    slider_time.set(timePlayed/1000)
    timer_text.configure(text="%02d:%02d"%((timePlayed/1000)//60,(timePlayed/1000)-((timePlayed/1000)//60)*60))

def change_loop_mode():
    global loopMode

    if loopMode == 3:
        loopMode = 0
    else:
        loopMode += 1
    loopImage.configure(light_image=Image.open(os.path.join(loopIconsPath, loopIconsList[loopMode][0])), dark_image=Image.open(os.path.join(loopIconsPath, loopIconsList[loopMode][1])))
    config.set('QOL', 'loop_mode', str(loopMode))
    with open(configPath, 'w') as configfile:
        config.write(configfile)

def init_music(song):
    global playingSong, timePlayed, paused
    if type(song) == int:
        playingSong = song

    #print(song, playingSong)

    pygame.mixer.music.load(os.path.join(filesDirectory, filesList[playingSong]))
    pygame.mixer.music.play()
    playButton.configure(text="PAUSE")
    paused = False
    timePlayed = 0
    slider_time.set(0)
    music_time = MP3(os.path.join(filesDirectory, filesList[playingSong])).info.length
    slider_time.configure(to=music_time, state="normal")
    timer_end_text.configure(text="%02d:%02d" % (music_time // 60, music_time - (music_time // 60) * 60))
    musicTitle.configure(text=("[", playingSong+1, "]", filesList[playingSong]))
    refresh_timePlayed(0, False)

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
            paused = False
            playButton.configure(text="PAUSE")
        else:
            playingSong = 0
            init_music(False)

        lastPlayed = time.time()*1000
        info_label.configure(text="")
    else:
        info_label.configure(text="You have no sound in the selected folder")

def next_music():
    global playingSong,timePlayed ,paused
    if songsCount > 1:
        if songsCount-1 > playingSong:
            playingSong += 1
        elif songsCount-1 == playingSong:
            playingSong = 0

        init_music(False)

    timePlayed = 0

def prev_music():
    global playingSong, timePlayed, paused
    if songsCount > 1:
        if playingSong > 0:
            playingSong -= 1
        elif playingSong == 0:
            playingSong = songsCount - 1

        init_music(False)

    timePlayed = 0

Windows = []
def open_window(name):
    global Windows

    for window in Windows:
        window.destroy()

    newWindow = customtkinter.CTkToplevel(app, fg_color=mainBackground_color)
    newWindow.title(name)
    newWindow.geometry("400x300")
    newWindow.minsize(400, 300)
    newWindow.resizable(False, False)

    newWindow.tkraise()
    newWindow.focus_force()
    newWindow.attributes("-topmost", True)

    newWindow.grid_columnconfigure(0, weight=1)
    newWindow.grid_rowconfigure(0, weight=1)

    scrollingFrame = customtkinter.CTkScrollableFrame(master=newWindow, fg_color=foreground_color, scrollbar_button_color=main_bars_color, scrollbar_button_hover_color=hover_bars_color)
    scrollingFrame.grid(padx=10, pady=10, column=0, row=0, sticky="ewns")
    scrollingFrame.grid_columnconfigure(0, weight=1)
    if name == "Settings":
        changeDirectoryButton = customtkinter.CTkButton(master=scrollingFrame, text="SELECT DIRECTORY", height=40, text_color=mainText_color, command=choose_directory, fg_color=clickable_color, hover_color=main_hover_color)
        changeDirectoryButton.grid(row=0, padx=20, pady=10, sticky="ew")

        darkModeButton = customtkinter.CTkButton(master=scrollingFrame, text="LIGHT/DARK MODE", height=40, text_color=mainText_color, command=change_color_mode, fg_color=clickable_color, hover_color=main_hover_color)
        darkModeButton.grid(row=1, padx=20, pady=10, sticky="ew")

    elif name == "Songs": # Shows all songs from the current selected directory
        for index, file in enumerate(os.listdir(filesDirectory)):
            button = customtkinter.CTkButton(master=scrollingFrame, text=file.lower(), height=40, fg_color=clickable_color, hover_color=main_hover_color, command=lambda i=index: init_music(i), text_color=mainText_color)
            button.grid(row=index, padx=20, pady=10, sticky="ew")

    elif name == "Create playlist":
        scrollingFrame.configure(height=250)
        scrollingFrame.grid(row=1, padx=20, pady=5, sticky="ew")
        newWindow.grid_rowconfigure(1, weight=1)
        newWindow.geometry("600x450")
        playlist_name_textbox = customtkinter.CTkTextbox(master=newWindow,
                                                         height=50,
                                                         text_color=mainText_color,
                                                         activate_scrollbars=False,
                                                         scrollbar_button_hover_color=hover_bars_color,
                                                         scrollbar_button_color=main_bars_color,
                                                         fg_color=clickable_color,
                                                         font=("",20),
                                                         wrap="none"
                                                         )
        playlist_name_textbox.grid(row=0, padx=20, pady=10, sticky="ewn")

        playlist_done_button = customtkinter.CTkButton(master=newWindow, height=50, text_color=mainText_color, text="Done", fg_color=clickable_color, hover_color=main_hover_color, font=("",20))
        playlist_done_button.configure(command=lambda: create_playlist(newWindow, playlist_name_textbox.get(0.0, "end")))
        playlist_done_button.grid(row=2, padx=20, pady=10, sticky="ewns")

        for index, file in enumerate(os.listdir(filesDirectory)):
            button = customtkinter.CTkButton(master=scrollingFrame, text=file.lower(), height=40, fg_color=unselected_color, hover_color=main_hover_color, text_color=mainText_color)
            button.configure(command=lambda b=button,i=index: select_song(b, i))
            button.grid(row=index, padx=20, pady=10, sticky="ew")

    elif name == "Playlists":
        scrollingFrame.grid(row=1)
        newWindow.grid_rowconfigure(1, weight=1)
        create_playlist_button = customtkinter.CTkButton(master=newWindow, text="NEW PLAYLIST", height=40, text_color=mainText_color, command=select_songs_to_create_playlist, fg_color=clickable_color, hover_color=main_hover_color)
        create_playlist_button.grid(row=0, padx=20, pady=10, sticky="ew")

        if playlists:
            print("not empty")
        else:
            print("empty")

    Windows.insert(len(Windows), newWindow)

playButton.configure(command=play_music)

openSettingsButton.configure(command=lambda: open_window("Settings"))
openMusicButton.configure(command=lambda: open_window("Songs"))
playlistButton.configure(command=lambda: open_window("Playlists"))

nextButton.configure(command=next_music)
previousButton.configure(command=prev_music)

loopButton.configure(command=change_loop_mode)

slider_time.configure(command=lambda x: [pygame.mixer.music.set_pos(slider_time.get()), refresh_timePlayed(slider_time.get(), True)])

def refresh_thread():
    global paused, playingSong, timePlayed
    while True:
        if pygame.mixer.music.get_busy():
            refresh_timePlayed(0, False)
        elif not paused:
            # print("finished")
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
                init_music(False)
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
                    init_music(False)
                    playButton.configure(text="PAUSE")
                    timePlayed = 0
                    paused = False
            elif loopMode == 3:
                if songsCount > 1:
                    randNum = random.randint(0,len(filesList)-1)
                    while randNum == playingSong:
                        randNum = random.randint(0,len(filesList)-1)
                    playingSong = randNum
                    init_music(False)
                    playButton.configure(text="PAUSE")
                    timePlayed = 0
                    paused = False
                else:
                    init_music(False)
                    playButton.configure(text="PAUSE")
                    timePlayed = 0
                    paused = False

        time.sleep(.05)

refreshThread = threading.Thread(target=refresh_thread)
refreshThread.start()

app.mainloop()

os._exit(0) # Stops the script from running after the main window's closed, preventing threads to keep on running after we close the app
