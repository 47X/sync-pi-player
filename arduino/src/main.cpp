#include <Arduino.h>
#include <Keyboard.h>

//IO config
#define audioLeft A1
#define audioRight A2
#define audioGnd A0
#define xlrPlay 2
#define xlrNext 3
#define xlrGnd 4
#define nextBtnIn 5
#define nextBtnGnd 6
#define playBtnIn 7
#define playBtnGnd 8
#define playBtnLed 9
#define builtinLed 13 //17 for pro micro

#define audioSensitivity 10

void playAction(){

}

void nextAction(){

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
