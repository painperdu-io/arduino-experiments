#!/usr/bin/python
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time

# define RGB-LED state
RGB_ENABLE = GPIO.LOW
RGB_DISABLE = GPIO.HIGH

# define RGB-LED pin
RGB_RED = 11
RGB_GREEN = 12
RGB_BLUE = 13

# define RGB-LED colors
RGB = [RGB_RED, RGB_GREEN, RGB_BLUE]
RGB_CYAN = [RGB_GREEN, RGB_BLUE]
RGB_MAGENTA = [RGB_RED, RGB_BLUE]
RGB_YELLOW = [RGB_RED, RGB_GREEN]
RGB_WHITE = [RGB_RED, RGB_GREEN, RGB_BLUE]


# Initialisation du GPIO
def initGPIO():
  # definition du mode
  GPIO.setmode(GPIO.BOARD)

  # definition des pins utilisées par la LED-RGB
  GPIO.setup(RGB_RED, GPIO.OUT, initial=RGB_DISABLE)
  GPIO.setup(RGB_GREEN, GPIO.OUT, initial=RGB_DISABLE)
  GPIO.setup(RGB_BLUE, GPIO.OUT, initial=RGB_DISABLE)


# Réinitialisation du GPIO
def cleanupGPIO():
  turnoffLED()
  GPIO.cleanup()


# Éteindre la LED-RGB
def turnoffLED():
  GPIO.output(RGB_RED, RGB_DISABLE)
  GPIO.output(RGB_GREEN, RGB_DISABLE)
  GPIO.output(RGB_BLUE, RGB_DISABLE)


# Définir une couleur
def setColorLED(color):
  turnoffLED()
  if isinstance(color, int):
    GPIO.output(color, RGB_ENABLE)
  else:
    for pin in color:
      GPIO.output(pin, RGB_ENABLE)


# Animation : clignotement de la LED
def animationBlinkLED(color, params):
  setColorLED(color)
  time.sleep(params[0])
  turnoffLED()
  time.sleep(params[1])


# Animation : allumer la LED
def animationColorLED(color, params):
  setColorLED(color)
  time.sleep(params[0])


# Animation : effet de fade in / fade out de la LED
def animationFadeLED(color, params):
  # en fonction du type de LED utilisée
  # le cycle vaut soit 0 ou 100 pour que
  # celle-ci soit à l'état off
  cycle = 0 if RGB_DISABLE == GPIO.LOW else 100

  # si la couleur est de type int
  # il faut la reconvertir en tableau
  if isinstance(color, int): color = [color]

  # initialisation PWM
  LED_RED = GPIO.PWM(RGB_RED, 50)
  LED_GREEN = GPIO.PWM(RGB_GREEN, 50)
  LED_BLUE = GPIO.PWM(RGB_BLUE, 50)

  # définir un cycle de départ
  LED_RED.start(cycle)
  LED_GREEN.start(cycle)
  LED_BLUE.start(cycle)

  # jouer l'animation sur la LED
  dc = cycle
  for i in range(0, 201, 1):
    # mise à jour du cycle sur la LED
    for rgb in color:
      if (rgb == RGB_RED):
        LED_RED.ChangeDutyCycle(dc)
      if (rgb == RGB_GREEN):
        LED_GREEN.ChangeDutyCycle(dc)
      if (rgb == RGB_BLUE):
        LED_BLUE.ChangeDutyCycle(dc)

    # incrementation du cycle
    if (dc == 100): incDc = -1
    if (dc == 0): incDc = 1
    dc += incDc

    # délai entre chaque cycle
    time.sleep(params[0])


  # reset PWM
  LED_RED.ChangeDutyCycle(cycle)
  LED_GREEN.ChangeDutyCycle(cycle)
  LED_BLUE.ChangeDutyCycle(cycle)

  LED_RED.stop()
  LED_GREEN.stop()
  LED_BLUE.stop()

  # délai entre chaque boucle de l'animation
  time.sleep(params[1])


# Passer d'un cycle de couleur à un autre
def colorFade(fromColor, toColor, time):
  # en fonction du type de LED utilisée
  # le cycle vaut soit 0 ou 100 pour que
  # celle-ci soit à l'état off
  cycleOff = 0 if RGB_DISABLE == GPIO.LOW else 100
  cycleOn = 100 if RGB_DISABLE == GPIO.LOW else 0

  # initialisation PWM
  LED_RED = GPIO.PWM(RGB_RED, 50)
  LED_GREEN = GPIO.PWM(RGB_GREEN, 50)
  LED_BLUE = GPIO.PWM(RGB_BLUE, 50)

  # initialisation des couleurs primaires
  if (fromColor == RGB_RED):
    LED_RED.ChangeDutyCycle(cycleOn)
  if (fromColor == RGB_GREEN):
    LED_GREEN.ChangeDutyCycle(cycleOn)
  if (fromColor == RGB_BLUE):
    LED_BLUE.ChangeDutyCycle(cycleOn)

  # jouer l'animation sur la LED
  dc = cycleOff
  for i in range(0, 101, 1):
    if (fromColor == RGB_RED):
      LED_RED.ChangeDutyCycle(cycleOn)
    if (fromColor == RGB_GREEN):
      LED_GREEN.ChangeDutyCycle(cycleOn)
    if (fromColor == RGB_BLUE):
      LED_BLUE.ChangeDutyCycle(cycleOn)

    if (fromColor == RGB_RED):
      LED_RED.ChangeDutyCycle(cycleOn)
    if (fromColor == RGB_GREEN):
      LED_GREEN.ChangeDutyCycle(cycleOn)
    if (fromColor == RGB_BLUE):
      LED_BLUE.ChangeDutyCycle(cycleOn)

    # délai entre chaque cycle
    time.sleep(params[0])

  # reset PWM
  LED_RED.ChangeDutyCycle(cycleOff)
  LED_GREEN.ChangeDutyCycle(cycleOff)
  LED_BLUE.ChangeDutyCycle(cycleOff)

  LED_RED.stop()
  LED_GREEN.stop()
  LED_BLUE.stop()


# Charger une animation pour la LED
def load(animation, color, params):
  if (animation == 'blink'):
    animationBlinkLED(color, params)
  if (animation == 'color'):
    animationColorLED(color, params)
  if (animation == 'fade'):
    animationFadeLED(color, params)


# Jouer une animaton sur la LED
def play(loop, animation, color, params):
  if (loop == -1):
    while 1:
      try:
        load(animation, color, params)
      except KeyboardInterrupt:
        pass
  else:
    for i in range (0, loop):
      load(animation, color, params)


# Main
def main():
  initGPIO()
  play(1, 'color', RGB_GREEN, [10])
  cleanupGPIO()


if __name__ == '__main__':
  main()
