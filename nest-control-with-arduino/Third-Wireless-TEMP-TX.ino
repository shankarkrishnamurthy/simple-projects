/* 
 * Temperature and humidity Wireless Transmitter
 * Using the DHT-22 and SHT21 sensor and nRF24L01 with Arduino uno
 * 
 * Author: Shankar K
 * Date: Dec 2017
 */

//Libraries
#include <Adafruit_Sensor.h>
#include <DHT.h>;
#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
#include <SHT21.h>

DHT dht(2, DHT22);
SHT21 sht;


/* RF
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

float Fahrenheit(float celsius) 
{
        return 1.8 * celsius + 32;
}

char *ftoa(char *a, double f, int precision)
{
 long p[] = {0,10,100,1000,10000,100000,1000000,10000000,100000000};
 
 char *ret = a;
 long heiltal = (long)f;
 itoa(heiltal, a, 10);
 while (*a != '\0') a++;
 *a++ = '.';
 long desimal = abs((long)((f - heiltal) * p[precision]));
 itoa(desimal, a, 10);
 return ret;
}

void setup()
{
    Serial.begin(115200);
    Wire.begin();    // begin Wire
    dht.begin();
    radio.begin();
    radio.openWritingPipe(address);
    radio.setPALevel(RF24_PA_MAX);
    radio.stopListening(); // Making it as Transmitter
}

void localPrint(char *s, float t, float h)
{
    Serial.print(s);
    Serial.print(" Humidity: ");
    Serial.print(h);
    Serial.print(" %, Temp: ");
    Serial.print(t);
    Serial.print(" C ");
    Serial.print(Fahrenheit(t));
    Serial.println(" F ");
}

void loop()
{
    //Variables
    int chk;
    float h1,h2;
    float t1,t2;
    const char text[64];
    char p1[8], f1[8];
    char p2[8], f2[8];

    //Read data and store it to variables hum and temp
    h1 = dht.readHumidity();
    t1= dht.readTemperature();
    //localPrint("DHT22", t1, h1);

    t2 = sht.getTemperature();  // get temp from SHT 
    h2 = sht.getHumidity(); // get temp from SHT
    //localPrint("SHT21", t2, h2);
    
    sprintf(text, "DHT22: %s T: %s F", 
                ftoa(p1, h1, 2), 
                ftoa(f1, Fahrenheit(t1), 2));
    Serial.println(text);
    radio.write(&text, sizeof(text));
        sprintf(text, "SHT21: %s T: %s F",  
                ftoa(p2, h2, 2), 
                ftoa(f2, Fahrenheit(t2), 2));
    Serial.println(text);
    radio.write(&text, sizeof(text));
    
    delay(30000); //Delay 30 sec.
}
