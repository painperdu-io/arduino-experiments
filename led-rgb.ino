/**
 * PAIN PERDU
 * --
 * Gestion de la LED
 */
#define PIN_LED_RED   9
#define PIN_LED_GREEN 10
#define PIN_LED_BLUE  11

/**
 * -- SETUP --
 */
void setup() {  
  //Serial.begin(9600);
  
  // définir les sorties de la LED
  pinMode(PIN_LED_RED, OUTPUT);
  pinMode(PIN_LED_GREEN, OUTPUT);
  pinMode(PIN_LED_BLUE, OUTPUT);

  // éteindre la LED
  setRGBColor(0, 0, 0);

  //int ledColor[] = {255, 0, 0};
  //int ledParams[] = {1, 5};
  //playLEDAnimation(3, "blink", ledColor, ledParams);
  //playLEDAnimation(-1, "fade", ledColor, ledParams);
}

/**
 * -- LOOP --
 */
void loop() 
{
 /*changeColor("blue", "red", 10);
 changeColor("red", "blue", 10);
 changeColor("blue", "green", 10);
 changeColor("green", "red", 10);
 changeColor("red", "blue", 10);*/
}

/**
 * Jouer une animation sur la LED
 * 
 * @param integer loop        nombre de fois que l'animation est joué (-1 si infini)
 * @param String  animation   nom de l'animation qui doit être joué
 * @param integer color[]     tableau des 3 couleurs RGB (de 0 à 255)
 * @param integer params[]    tableau de paramètres de l'anomation
 */
void playLEDAnimation(int loop, String animation, int color[], int params[]) 
{
  int i = 0;
  if (loop == -1) {
    while(true) {
      loadLEDAnimation(animation, color, params);
    }
  }
  else {
    for (i = 0 ; i < loop ; i++) {
      loadLEDAnimation(animation, color, params);
    }
  } 
}

/**
 * Charger une animation pour la LED
 * 
 * @param String  animation   nom de l'animation qui doit être joué
 * @param integer color[]     tableau des 3 couleurs RGB (de 0 à 255)
 * @param integer params[]    tableau de paramètres de l'anomation
 */
void loadLEDAnimation(String animation, int color[], int params[])
{
  if (animation == "blink") {
    blinkLED(color, params);
  }
  if (animation == "fade") {
    fadeLED(color, params);
  }
}

/**
 * Définir la couleur rouge de la LED
 * 
 * @param integer red   variation de couleur de 0 à 255
 */
void setRedColor(int red)
{
  analogWrite(PIN_LED_RED, 255 - red);
}

/**
 * Définir la couleur verte de la LED
 * 
 * @param integer green   variation de couleur de 0 à 255
 */
void setGreenColor(int green)
{
  analogWrite(PIN_LED_GREEN, 255 - green);
}

/**
 * Définir la couleur bleu de la LED
 * 
 * @param integer blue    variation de couleur de 0 à 255
 */
void setBlueColor(int blue)
{
  analogWrite(PIN_LED_BLUE, 255 - blue);
}

/**
 * Définir la couleur RGB de la LED
 * 
 * @param integer red     variation de couleur de 0 à 255
 * @param integer green   variation de couleur de 0 à 255
 * @param integer blue    variation de couleur de 0 à 255
 */
void setRGBColor(int red, int green, int blue)
{
  setRedColor(red);
  setGreenColor(green);
  setBlueColor(blue);
}

/**
 * Animation : clignotement de la LED
 */
void blinkLED(int color[], int params[])
{
    setRGBColor(color[0], color[1], color[2]);
    delay(params[0]);
    setRGBColor(0, 0, 0);
    delay(params[1]);
}

/**
 * Animation : effet de fade in / fade out de la LED
 */
void fadeLED(int color[], int params[]) 
{
  int i;
  int initRed   = color[0];
  int initGreen = color[1];
  int initBlue  = color[2];
  int incRed    = (color[0] == 0) ? 0 : -1;
  int incGreen  = (color[1] == 0) ? 0 : -1;
  int incBlue   = (color[2] == 0) ? 0 : -1;

  // initialiser et éteindre la LED
  color[0] = 0;
  color[1] = 0;
  color[2] = 0;
  setRGBColor(color[0], color[1], color[2]);

  // réaliser l'effet de fade in / fade out
  for (i = 0 ; i < 510 ; i++) {

    // changer le sens d'incrementation
    if (color[0] == 0 || color[0] == 255) {
      incRed = -incRed;
    }
    if (color[1] == 0 || color[1] == 255) {
      incGreen = -incGreen;
    }
    if (color[2] == 0 || color[2] == 255) {
      incBlue = -incBlue;
    }

    // mettre à jour la couleur
    color[0] += incRed;
    color[1] += incGreen;
    color[2] += incBlue; 
    setRGBColor(color[0], color[1], color[2]);

    // effet sur la variation
    delay(params[0]);
  }

  // redéfinir la couleur d'origine
  color[0] = initRed;
  color[1] = initGreen;
  color[2] = initBlue;

  // délai avant une nouvelle animation
  delay(params[1]);
}

/**
 * Changer la couleur de la LED d'une couleur 
 * primaire à une autre avec variation.
 */
void changeColor(String from, String to, int time) 
{
  int i;
  int red;
  int green;
  int blue;

  // initialiser les couleurs primaires
  red   = (from == "red")   ? 255 : 0;
  green = (from == "green") ? 255 : 0;
  blue  = (from == "blue")  ? 255 : 0;

  // passer d'une couleur primaire à une autre
  for (i = 0; i < 255; i += 1) {

    if (from == "red") red -= 1;
    if (from == "green") green -= 1;
    if (from == "blue") blue -= 1;
    if (to == "red") red += 1;
    if (to == "green") green += 1;
    if (to == "blue") blue += 1;

    // varier les couleurs primaires
    if (from == "red" || to == "red") {
      setRedColor(red);
    }
    if (from == "green" || to == "green") {
      setGreenColor(green);
    }
    if (from == "blue" || to == "blue") {
      setBlueColor(blue);
    }

    // attendre entre chaque variation
    delay(time);
  }
}
