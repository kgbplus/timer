#!/usr/bin/python
# -*- coding: utf-8 -*-

RASPI = True
NO_PICT = True

import os, pygame
from pygame.locals import *
from subprocess import Popen 
from datetime import datetime
if RASPI:
  import RPi.GPIO as GPIO

# GPIO setup
if RASPI:
  GPIO.setmode(GPIO.BCM)
  But1 = 16
  But2 = 19
  But3 = 20
  But4 = 21
  But5 = 26
  GPIO.setup(But1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
  GPIO.setup(But2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
  GPIO.setup(But3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
  GPIO.setup(But4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
  GPIO.setup(But5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
  
  Relay1 = 18
  Relay2 = 27
  GPIO.setup(Relay1, GPIO.OUT)
  GPIO.output(Relay1, False)
  GPIO.setup(Relay2, GPIO.OUT)
  GPIO.output(Relay2, False)
else:
  pygame.mixer.init()
  alert = pygame.mixer.Sound('bell.wav')
  But1 = K_F1
  But2 = K_F2
  But3 = K_F3
  But4 = K_F4
  But5 = K_F5
  Relay1 = 18
  Relay2 = 27

pygame.init()
os.environ['SDL_VIDEO_WINDOW_POS'] = 'center'
pygame.display.set_caption("TIMER")
screen = pygame.display.set_mode([1920,1080],pygame.FULLSCREEN)
pygame.mouse.set_visible(0)
clock = pygame.time.Clock()

# Define some colours
white = (255,255,255); black = (0,0,0); yellow = (255,255,0); red = (255,0,0) 

bg = pygame.Surface(screen.get_size())
bg = bg.convert()
bg.fill(black)
screen.blit(bg, (0, 0))
pygame.display.flip()
	
running = True
But4_pressed = False

if RASPI:
  wait = pygame.image.load("/home/pi/timer/wait.png")
  intro = pygame.image.load("/home/pi/timer/intro.png")
  loose = pygame.image.load("/home/pi/timer/loose.png")
  win = pygame.image.load("/home/pi/timer/win.png")
  #other = pygame.image.load("/home/pi/timer/other.png")

  intro_video_path = "/home/pi/timer/intro.mp4"
  loose_video_path = "/home/pi/timer/loose.mp4"
  win_video_path = "/home/pi/timer/win.mp4"
  other_video_path = "/home/pi/timer/other.mp4"
else:
  wait = pygame.image.load("wait.png")
  intro = pygame.image.load("intro.png")
  loose = pygame.image.load("loose.png")
  win = pygame.image.load("win.png")
  #other = pygame.image.load("other.png")

  intro_video_path = "intro.avi"
  loose_video_path = "loose.avi"
  win_video_path = "win.avi"
  other_video_path = "other.avi"


def write(msg,color):
    if RASPI:
      myfont = pygame.font.Font("/home/pi/timer/digital-7 (mono).ttf", 435)
    else:
      myfont = pygame.font.Font("digital-7 (mono).ttf", 435)
    myfont.set_bold(False)
    mytext = myfont.render(msg, True, color)
    mytext = mytext.convert_alpha()
    return mytext
	
def exit():
  if (RASPI):
    GPIO.cleanup()
  pygame.quit()
  
def clear_screen():
  screen.fill(black)
  pygame.display.flip()
  
def show_pict(pict):
  if NO_PICT:
	  clear_screen()
  else:
	  screen.blit(pict,[0,0])
	  pygame.display.flip()
  
def play_video(video_path):
  if RASPI:
    proc = Popen("exec /usr/bin/omxplayer -o both " + video_path,shell=True)
    proc.wait()

def show_timer():

  global But4_pressed
  counting = True
  start_mc = pygame.time.get_ticks()

  while counting:
    for i in pygame.event.get():
      if i.type == QUIT or (i.type == KEYDOWN and i.key == K_ESCAPE):
        counting = False

    if RASPI:
      if(GPIO.input(But4)):
        pygame.time.delay(80)
        if (GPIO.input(But4)):
          counting = False
          But4_pressed = True

    screen.fill(black)
    
    ms_left = 5 * 60 * 1000 + start_mc - pygame.time.get_ticks()
    if (ms_left<500):
      ms_left = 0
      counting = False
      
    minutes = ms_left // 60000
    seconds = (ms_left // 1000) % 60
    mks = (ms_left % 1000) /10

    output_text = "{0:02}:{1:02}:{2:02}".format(minutes,seconds,mks)
    
    timer_text = write(output_text,red)
    screen.blit(timer_text,[150,1080/2 - 200])
 
    pygame.display.flip()
    
def timedef_sec(dt):
  return dt.total_seconds()

def check_but_state():
  start_time = datetime.now()
  while (timedef_sec(datetime.now() - start_time) <= 0.1):  # BUTTON CONNECTION WAIT TIME !!!!!!!!!!!!!!!
    if RASPI:
      if (not GPIO.input(SWITCH)):
        return False
  return True 

def switch_on_relay(relay):
  if RASPI:
    GPIO.output(relay, True)
    pygame.time.delay(1000)
    GPIO.output(relay, False)
  else:
    alert.play()
    
def wait_one_but(but):
  ready = False
  if RASPI:
    while (not ready):
      if(GPIO.input(but)):
        pygame.time.delay(80)
        if (GPIO.input(but)):
          ready = True
  else:
    while (not ready):    
      for i in pygame.event.get():
        if (i.type == KEYDOWN and i.key == but):
          ready = True

def wait_two_but(but1,but2):
  ready = False
  if RASPI:
    while (not ready):
      if(GPIO.input(but1)):
        pygame.time.delay(80)
        if (GPIO.input(but1)):
          ready = True
          pygame.time.delay(1500)
          if (GPIO.input(but2)):
            return False
  else:
    while (not ready):    
      for i in pygame.event.get():
        if (i.type == KEYDOWN and i.key == but1):
          ready = True
          pygame.time.delay(1500)
          for i in pygame.event.get():
            if (i.type == KEYDOWN and i.key == but2):
              return False
  return True

while running:
  show_pict(wait)
  
  wait_one_but(But1)
  
  switch_on_relay(Relay1)
  play_video(intro_video_path)
  show_pict(intro)
  
  if (wait_two_but(But2,But3)):
    play_video(loose_video_path)
    show_timer()
    switch_on_relay(Relay2)
    show_pict(loose)
  else:
    switch_on_relay(Relay2)
    play_video(win_video_path)
    show_pict(win)
  
  if (not But4_pressed):
    wait_one_but(But4)
  else:
    But4_pressed = False
  
  for i in pygame.event.get():
   if i.type == QUIT or (i.type == KEYDOWN and i.key == K_ESCAPE):
    running = False
  
