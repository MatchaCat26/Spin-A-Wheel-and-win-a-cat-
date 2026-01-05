import pygame, os
 
#initialize pygame mixer once
pygame.mixer.init()

#base path
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SOUND_DIR = os.path.join(BASE_DIR,"assets")

#load sounds
spin_sound = pygame.mixer.Sound(os.path.join(SOUND_DIR,"spin_sound.mp3"))
win_sound = pygame.mixer.Sound(os.path.join(SOUND_DIR,"pop-up_sound.mp3"))
button_sound = pygame.mixer.Sound(os.path.join(SOUND_DIR,"button_sound.mp3"))
confetti_sound = pygame.mixer.Sound(os.path.join(SOUND_DIR,"confetti-very-loud-explosion_sound.mp3"))

#volume tuning
spin_sound.set_volume(0.75)
button_sound.set_volume(0.5)
confetti_sound.set_volume(0.8)

#sound control functions
def play_spin():
    #loop the spinning sound
    spin_sound.play(loops=-1)
def stop_spin():
    spin_sound.stop()

def play_win():
    win_sound.play()

def play_button():
    button_sound.play()

def play_confetti():
    confetti_sound.play()
