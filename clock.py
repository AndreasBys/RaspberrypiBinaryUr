#!/usr/bin/env python
'''Velkommen til mit program: clock.py'''

'''Imports'''
import sys
from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
hat = SenseHat()
import signal 
import time, datetime



hour_color = (0, 255, 0)
minute_color = (0, 0, 255)
second_color = (255, 0, 0)
off = (0, 0, 0)

t = datetime.datetime.now()

'''Dette er en global variable som jeg så sætter via argv hvis inputtet fra useren er valid (Ikke string og et tal fra 0-1), Formattet ændrer kolonner'''
format = 0
try:
    format = int(sys.argv[1])
    if format >= 2:
        format = 0
except:
    format = 0
    
'''Global function sætter AM/PM eller militær tid, tager et input fra 0-1'''
AmericaTime = 0
try:
    AmericaTime = int(sys.argv[2])
    if AmericaTime >= 2:
        AmericaTime = 0
except:
    AmericaTime = 0
'''Sætter rotation, den tager inputtet 0 eller 90, som er graderne.'''
Rotation = 0
try:
    Rotation = int(sys.argv[3])
    if Rotation == 0 or Rotation == 90:
        Rotation = Rotation
except:
    Rotation = 0
'''En global function som styrer om klokken slår, ændres senere til false når jeg stopper programmet'''
Running = True

hat.clear()


def pushed_down(event):
    '''Function som aktiverer når joystick bliver skubbet ned, skifter til AM/PM, den tager imod et push event fra hat.direction
    
    params
        event: et event objekt fra hat.direction'''
    hat.clear()
    global AmericaTime
    if event.action == ACTION_RELEASED:
        if AmericaTime == 0:
            AmericaTime = 1
        else:
            AmericaTime = 0


def pushed_left(event):
    '''Når joysticken bliver skubbet venstre skifter kolonne mængder, den tager imod et push event fra hat.direction'''
    hat.clear()
    global format
    if event.action == ACTION_RELEASED:
        if format == 0:
            format = 1
        else:
            format = 0

def pushed_right(event):
    '''Når joysticken bliver skubbet højre skifter vi rotationen, den tager imod et push event fra hat.direction'''
    hat.clear()
    global Rotation
    if event.action == ACTION_RELEASED:
        if Rotation == 0:
            Rotation = 90
        else:
            Rotation = 0


def display_binary(value, row, color):
    '''Functionen til at display tid i binært, her tager jeg imod et tal som lavet om til binært, en row som er hvor min pixel skal placeres og en tuple med 3 farver tal(RGB)'''
    binary_str = "{0:8b}".format(value)
    for x in range(0, 8):
        if binary_str[x] == '1':
            hat.set_pixel(x, row, color[0], color[1], color[2])
        else:
            hat.set_pixel(x, row, 0, 0, 0)


def threecolumn24hr():
    '''Denne function viser tiden på tre kolumner'''
    global Rotation
    hat.set_rotation(Rotation)
    t = datetime.datetime.now()
    global AmericaTime
    if AmericaTime == 1:
        hat.set_pixel(0,0,255,0,0)
        if t.hour > 12:
            timer = t - datetime.timedelta(hours=12)
            t = timer
    display_binary(t.hour, 3, hour_color)
    display_binary(t.minute, 4, minute_color)
    display_binary(t.second, 5, second_color)


def sixcolumn24hr():
    '''Denne function viser 6 kolumner af tiden, '''
    global Rotation
    hat.set_rotation(Rotation)

    t = datetime.datetime.now()
    global AmericaTime
    if AmericaTime == 1:
        hat.set_pixel(0,0,255,0,0)
        if t.hour > 12:
            timer = t - datetime.timedelta(hours=12)
            t = timer


    try:
        time1 = int(str(t.hour)[0:1])
    except:
        time1 = 0
    try: 
        time2 = int(str(t.hour)[1:2:])
    except:
        time2 = 0
    try:
        minut1 = int(str(t.minute)[0:1])
    except:
        minut1 = 0
    try:
        minut2 = int(str(t.minute)[1:2:])
    except:
        minut2 = 0
    try: 
        sekundt1 = int(str(t.second)[0:1])
    except: 
        sekundt1 = 0
    try:
        sekundt2 = int(str(t.second)[1:2:])
    except:
        sekundt2 = 0

    display_binary(time1,1,hour_color)
    display_binary(time2,2,hour_color)

    display_binary(minut1,3, minute_color)
    display_binary(minut2,4, minute_color)

    display_binary(sekundt1,5,second_color)
    display_binary(sekundt2,6,second_color)

def exit_up():
    global Running
    Running = False

def signal_term_handler(signal, frame):
    '''Dette er en function som tager imod værdier fra signal, denne process kigger efter et Kill'''
    print("Programmet slutter")
    hat.show_message("Programmet slutter")
    sys.exit(0)
 
signal.signal(signal.SIGTERM, signal_term_handler)
'''Signal kigger efter et specifikt input commandsne, denne kigger efter et Kill'''

def signal_INT_handler(signal, frame):
    '''Dette er en function som tager imod værdier fra signal, denne process kigger efter et keyboard interrupt'''
    print("Programmet slutter")
    hat.show_message("Programmet slutter")
    sys.exit(0)
 
signal.signal(signal.SIGINT, signal_INT_handler)
'''Signal kigger efter et specifikt input commandsne, denne kigger efter et Keyboard interrupt'''

hat.stick.direction_up = exit_up
hat.stick.direction_down = pushed_down
hat.stick.direction_left = pushed_left
hat.stick.direction_right = pushed_right

def main():
    '''Dette er main-loopet, det kører indtil at der er lavet et joystick-up eller en kill/interrupt command'''
    hat.show_message("Programmet starter")
    while Running:
        if format == 0:
            sixcolumn24hr()
        else:
            threecolumn24hr()
        time.sleep(1)
    hat.show_message("Programmet slutter")
    hat.clear()
    sys.exit(0)

if __name__ == "__main__":
    main()

