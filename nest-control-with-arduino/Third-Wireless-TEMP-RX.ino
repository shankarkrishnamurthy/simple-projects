#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
#include <DS3231.h>

/*
VCC<->3.3 V
GND<->GND
MOSI<->D11
MISO<->D12
SCK<->D13
CE<->D7
CSN<->D8
*/
RF24 radio(7, 8); // CE, CSN
const byte address[6] = "00001";


DS3231 Clock;
bool Century=false,  h12, PM;

void ReadDS3231()
{
  int second,minute,hour,date,month,year,temperature; 
  second=Clock.getSecond();
  minute=Clock.getMinute();
  hour=Clock.getHour(h12, PM);
  date=Clock.getDate();
  month=Clock.getMonth(Century);
  year=Clock.getYear();
  
  temperature=Clock.getTemperature();
    
  Serial.print(" 20");
  Serial.print(year,DEC);
  Serial.print('-');
  Serial.print(month,DEC);
  Serial.print('-');
  Serial.print(date,DEC);
  Serial.print(' ');
  Serial.print(hour,DEC);
  Serial.print(':');
  Serial.print(minute,DEC);
  Serial.print(':');
  Serial.print(second,DEC);
  Serial.print(";LocalTemp@recv=");
  Serial.print(temperature); 
  Serial.print("; ");
}


void setup() {
  Serial.begin(115200);
  Wire.begin(); // needed for clock to work
  radio.begin();
  radio.openReadingPipe(0, address);
  radio.setPALevel(RF24_PA_MAX);
  radio.startListening(); // Making it as receiver
}

void loop() {
  ReadDS3231();
  if (radio.available()) {
    char text[32] = "";
    radio.read(&text, sizeof(text));
    Serial.println(text);
  }
}
