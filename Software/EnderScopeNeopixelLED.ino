#include <Adafruit_NeoPixel.h>

#define PIN            6  // Define the pin to which your NeoPixel strip is connected
#define NUM_LEDS       16 // Define the number of NeoPixels in your strip
#define BUTTON_PIN     2  // Define the pin where the push button is connected

Adafruit_NeoPixel strip = Adafruit_NeoPixel(NUM_LEDS, PIN, NEO_GRB + NEO_KHZ800);

int buttonState = HIGH;
int lastButtonState = HIGH;
unsigned long lastDebounceTime = 0;
unsigned long debounceDelay = 50;
bool ledOn = false;

void setup() {
  strip.begin();
  strip.show(); // Initialize all pixels to 'off'
  pinMode(BUTTON_PIN, INPUT_PULLUP);
}

void loop() {
  int reading = digitalRead(BUTTON_PIN);
  if (reading != lastButtonState) {
    lastDebounceTime = millis();
  }

  if ((millis() - lastDebounceTime) > debounceDelay) {
    if (reading != buttonState) {
      buttonState = reading;

      if (buttonState == LOW) {
        // Button was pressed
        if (ledOn) {
          turnWhite(); // Turn NeoPixels white
          ledOn = false;
        } else {
          turnGreen(); // Turn NeoPixels green
          ledOn = true;
        }
      }
    }
  }

  lastButtonState = reading;
}

void turnGreen() {
  for (int i = 0; i < NUM_LEDS; i++) {
    strip.setPixelColor(i, 0, 255, 0); // Green color
  }
  strip.show();
}

void turnWhite() {
  for (int i = 0; i < NUM_LEDS; i++) {
    strip.setPixelColor(i, 255, 255, 255); // White color
  }
  strip.show();
}

