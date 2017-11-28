#include <Arduino.h>
#include <Keyboard.h>

//IO config
#define audioLeft A0 //brown, 10k pulldown to A1 set as gnd
#define audioRight A2 //red, 10k pulldown to A1 set as gnd
#define audioGnd A1 //white or any marked special, run out of colors
#define xlrPlayIn 2 //black
#define xlrNextIn 3 //gray
#define xlrGnd 4 //white
#define nextBtnIn 5 //yellow
#define nextBtnGnd 6 //orange
#define playBtnIn 7 //purple
#define playBtnGnd 8 //blue
#define playBtnLed 9 //green, PWM
#define builtinLed 17 //13 for leonardo, 17 for pro micro

#define audioSensitivity 10

void playAction(){
  //Serial.println("play action");
  Keyboard.print('p');
}

void nextAction(){
  //Serial.println("next action");
  Keyboard.print('n');
}

void setup() {
    //setup communications
    //Serial.begin(9600);
    Keyboard.begin();
    //setup pin modes
    pinMode(audioLeft, INPUT);
    pinMode(audioRight, INPUT);
    pinMode(audioGnd, OUTPUT);
    pinMode(xlrPlayIn, INPUT_PULLUP);
    pinMode(xlrNextIn, INPUT_PULLUP);
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
    //blink led few times to show that we are ready
    for (size_t i = 0; i < 10; i++) {
      digitalWrite(playBtnLed, 1);
      delay(200);
      digitalWrite(playBtnLed, 0);
      delay(100);
    }
}

//globals for reading state
int audioPlay;
int audioNext;
bool buttonPlay;
bool buttonNext;
bool xlrPlay;
bool xlrNext;

void loop() {
  //read audio
  audioPlay = analogRead(audioLeft);
  audioNext = analogRead(audioRight);
  //read buttons and xlr
  buttonPlay =! digitalRead(playBtnIn);
  buttonNext =! digitalRead(nextBtnIn);
  xlrPlay =! digitalRead(xlrPlayIn);
  xlrNext =! digitalRead(xlrNextIn);
  //if audio > audioSensitivity or btns or pins execute action and wait
  if (audioPlay > audioSensitivity or buttonPlay or xlrPlay) {
    playAction();
    //blink once
    digitalWrite(playBtnLed, 1);
    delay(300);
    digitalWrite(playBtnLed, 0);
    delay(100);
  }
  if (audioNext > audioSensitivity or buttonNext or xlrNext) {
    nextAction();
    //blink twice
    digitalWrite(playBtnLed, 1);
    delay(100);
    digitalWrite(playBtnLed, 0);
    delay(100);
    digitalWrite(playBtnLed, 1);
    delay(100);
    digitalWrite(playBtnLed, 0);
    delay(100);
  }
  //wait 1ms in loop anyway?
  //Serial.print(audioPlay);
  //Serial.print(" ");
  //Serial.println(audioNext);
  //delay(1);
}
