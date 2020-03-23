#include <IRremote.h>
#include <IRremoteInt.h>

int RECV_PIN = 13;
IRrecv receiver(RECV_PIN); 
decode_results results;

void setup() {
  Serial.begin(9600);
  Serial.println("started");
  receiver.enableIRIn();
}

void loop() {
  if(receiver.decode(&results)) {
    Serial.println(results.value, HEX);
    receiver.resume();
  }
}
