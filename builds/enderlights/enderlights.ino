/*
  Enderlights

  Firmware for an Enderscope illumination device
  Accepts commands over the serial port so that Neopixels can be driven programatically
  S0 shutter Off
  S1 sutter On
  A80 all (r,g,b) set to 80
  R30 r set to 30
  G50
  B255
  MA, MR, MG, MB : set a 16-bit binary mask value to enable/disable specific LEDs
  ? query current r,g,b values
  A button cycles through some standart modes.

  Author: Jerome Mutterer (jerome.mutterer[at]cnrs.fr)
  2024-06-06: v1.03 add the ? state query command

*/

#include <Adafruit_NeoPixel.h>

int neoPin = 9;
int buttonPin = 4;
int numPixels = 12;
int r, g, b, mr, mg, mb, mode;  
String cmd, resp;
int shutter = 0;
char eol = '\n';

Adafruit_NeoPixel *pixels;

void setup() {
  pinMode(buttonPin,INPUT_PULLUP);
  Serial.begin(9600);
  while (!Serial) {
    ;
  }
  pixels = new Adafruit_NeoPixel(numPixels, neoPin, NEO_GRB + NEO_KHZ800);
  pixels->begin();
  shutter = 1;
  mr = mg = mb = 65535;
  r = g = b = 100;
  updatePixels();
  mode=0;
}

void loop() {

  if (Serial.available() > 0) {
    cmd = Serial.readStringUntil(eol);
    resp = "ok";
    if (cmd.startsWith("S")) {
      shutter = (cmd.substring(1).toInt() == 0) ? 0 : 1;
    } else if (cmd.startsWith("MR")) {
      mr = cmd.substring(2).toInt();
    } else if (cmd.startsWith("MG")) {
      mg = cmd.substring(2).toInt();
    } else if (cmd.startsWith("MB")) {
      mb = cmd.substring(2).toInt();
    } else if (cmd.startsWith("MA")) {
      mr = mg = mb = cmd.substring(2).toInt();
    } else if (cmd.startsWith("R")) {
      r = cmd.substring(1).toInt();
    } else if (cmd.startsWith("G")) {
      g = cmd.substring(1).toInt();
    } else if (cmd.startsWith("B")) {
      b = cmd.substring(1).toInt();
    } else if (cmd.startsWith("A")) {
      r = g = b = cmd.substring(1).toInt();
    } else if (cmd.startsWith("?")) {
      resp = "RGB:"+String(r)+";"+String(g)+";"+String(b);
    } else {
      resp = "Err";
    }
    cmd = "";
    Serial.println(resp);
    updatePixels();
  }
  if(digitalRead(buttonPin)==LOW) {
    mode = (mode+1)%5;
    if ( mode==1) {
        r=255;g=255;b=255;
    } else if ( mode==2) {
        r=255;g=0;b=0;
    } else if ( mode==3) {
        r=0;g=255;b=0;
    } else if ( mode==4) {
        r=0;g=0;b=255;
    } else if ( mode==0) {
        r=0;g=0;b=0;
    } 
    updatePixels();
    delay(100);
  }
}

void updatePixels() {
  pixels->clear();
  for (int i = 0; i < numPixels; i++) {
    pixels->setPixelColor(i,
                          pixels->Color(shutter * r * ((mr >> i) & 1),
                                        shutter * g * ((mg >> i) & 1),
                                        shutter * b * ((mb >> i) & 1)));
  }
  pixels->show();
}
