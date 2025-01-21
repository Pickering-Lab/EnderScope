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
  M 1 switches to sectors only mode
  p 5 select which sector to use. bits in parameter encode sectors
  M 2 switches to single LED mode
  P 10 select which LED to use 0..numPixels
  ? query current r,g,b values

  Authors: Jerome Mutterer (jerome.mutterer[at]cnrs.fr), 
           Erwan Grandgirard (grandgie[at]igbmc.fr) 
  2024-06-06: v1.03 add the '?' state query command
  2024-12-03: v1.04 remove button; add 'm' and 'p' commands for mode and parameter

*/

#include <Adafruit_NeoPixel.h>

int neoPin = 9;
int numPixels = 12;
int r, g, b, mr, mg, mb, mode, parameter;
String cmd, resp;
int shutter = 0;
char eol = '\n';

Adafruit_NeoPixel *pixels;

void setup() {
  Serial.begin(57600);
  while (!Serial) {
    ;
  }
  pixels = new Adafruit_NeoPixel(numPixels, neoPin, NEO_GRB + NEO_KHZ800);
  pixels->begin();
  shutter = 0;
  mr = mg = mb = 65535;
  r = g = b = 20;
  updatePixels();
  mode = 0;
  parameter = 0;
}

void loop() {

  if (Serial.available() > 0) {
    cmd = Serial.readStringUntil(eol);
    resp = "ok";
    cmd.toLowerCase();
    if (cmd.startsWith("s")) {
      shutter = (cmd.substring(1).toInt() == 0) ? 0 : 1;
    } else if (cmd.startsWith("mr")) {
      mr = cmd.substring(2).toInt();
    } else if (cmd.startsWith("mg")) {
      mg = cmd.substring(2).toInt();
    } else if (cmd.startsWith("mb")) {
      mb = cmd.substring(2).toInt();
    } else if (cmd.startsWith("ma")) {
      mr = mg = mb = cmd.substring(2).toInt();
    } else if (cmd.startsWith("r")) {
      r = cmd.substring(1).toInt();
    } else if (cmd.startsWith("g")) {
      g = cmd.substring(1).toInt();
    } else if (cmd.startsWith("b")) {
      b = cmd.substring(1).toInt();
    } else if (cmd.startsWith("a")) {
      r = g = b = cmd.substring(1).toInt();
    } else if (cmd.startsWith("m")) {
      mode = cmd.substring(1).toInt();
    } else if (cmd.startsWith("p")) {
      parameter = cmd.substring(1).toInt();
    } else if (cmd.startsWith("?")) {
      resp = "RGB:" + String(r) + ";" + String(g) + ";" + String(b);
    } else {
      resp = "Err";
    }
    cmd = "";

    // example mode and parameter implementation
    // mode 1 creates masks for using only quarter ring sectors
    // param value bits indicate which sector to use, eg: 5 = sector 1 + 4
    if (mode == 1) {
      int mask = 0x00;
      for (int i = 0; i < 4; i++)
        for (int j = 0; j < numPixels / 4; j++) {
          if ((parameter >> i)&B1) mask = mask | (B1 << (i * numPixels / 4) + j);
        }
      mr = mg = mb = mask;
    } else if (mode == 2) { // single LED mode
      mr = mg = mb = B1 << parameter;
    } else if (mode == 3) {
      // implement other modes here
    }
    updatePixels();
    Serial.println(resp);
  }
  delay(1);
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
