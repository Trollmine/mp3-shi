#Mp3 reader V1:
import pygame
import pathlib
import time
import threading
import os

filesDirectory = r"/home/mathis.rocheg@fbuisson2.peda/Documents/mp3-shi/Songs"
initialCount   = 0

for path in pathlib.Path("/home/mathis.rocheg@fbuisson2.peda/Documents/mp3-shi/Songs").iterdir():
    if path.is_file():
        initialCount += 1

fileslist = os.listdir(filesDirectory)

print(initialCount, ": ", fileslist)

def play_music(file):
    pygame.mixer.init()
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()

def wait_for_input():
    input("stop?")
    pygame.mixer.music.stop()

question = "Choose a song between: \n"
for i in range(initialCount):
    question = question + "["+ str(i) +"]" + str(fileslist[i])+"\n"


songNum = input(question)
path = os.path.join(filesDirectory, fileslist[int(songNum)])

music_thread = threading.Thread(target=play_music, args=(path,))
input_thread = threading.Thread(target=wait_for_input)

music_thread.start()
input_thread.start()

