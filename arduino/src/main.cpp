#include <Arduino.h>
#include <Keyboard.h>

//IO config
#define audioLeft A0 //brown, 10k pulldown to A1 set as gnd
#define audioRight A2 //white or any marked special
#define audioGnd A1 //red, 10k pulldown to A1 set as gnd
#define xlrPlay 2 //black
#define xlrNext 3 //gray
#define xlrGnd 4 //white
#define nextBtnIn 5 //yellow
#define nextBtnGnd 6 //orange
#define playBtnIn 7 //purple
#define playBtnGnd 8 //blue
#define playBtnLed 9 //green, PWM
#define builtinLed 17 //13 for leonardo, 17 for pro micro

#define audioSensitivity 10

void playAction(){
  Serial.println("play action");
}

void nextAction(){
  Serial.println("next action");
}

void setup() {
    //setup communications
    Serial.begin(9600);
    Keyboard.begin();
    //setup pin modes
    pinMode(audioLeft, INPUT);
    pinMode(audioRight, INPUT);
    pinMode(audioGnd, OUTPUT);
    pinMode(xlrPlay, INPUT_PULLUP);
    pinMode(xlrNext, INPUT_PULLUP);
    pinMode(xlrGnd, OUTPUT);
    pinMode(nextBtnIn, INPUT_PULLUP);
    pinMode(nextBtnGnd, OUTPUT);
    pinMode(playBtnIn, INPUT_PULLUP);
    pinMode(playBtnGnd, OUTPUT);
    pinMode(playBtnLed, OUTPUT);
    pinMode(builtinLed, OUTPUT);
    //set GND pins to low
    digitalWrite(audioGnd, 0);
    digitalWrite(xlrGnd, 0);
    digitalWrite(nextBtnGnd, 0);
    digitalWrite(playBtnGnd, 0);
}

void loop() {
  //read audio
  //read buttons and xlr
  //if audio > audioSensitivity or btns or pins execute action and wait
  //wait 1ms in loop anyway

}
