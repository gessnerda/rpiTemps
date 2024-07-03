#include <LiquidCrystal.h>
#include <DHT.h>
#define DHTPIN 2
#define DHTTYPE DHT11

LiquidCrystal lcd(7, 8, 9, 10, 11, 12);

DHT dht(DHTPIN, DHTTYPE);

const int numPIs = 4;
float cpuTemps[numPIs];
String piNames[numPIs] = {"devpi", "devpi2", "rasballs", "rasballs2"};
int currentDisplay = 0; 

void setup() {
  Serial.begin(9600);
  lcd.begin(16, 2);
  dht.begin();
}

void loop() {
  if (Serial.available()) {
    String cpuTempStr = Serial.readStringUntil('\n');
    int piIndex = cpuTempStr.charAt(0) - '0';
    cpuTemps[piIndex] = cpuTempStr.substring(2).toFloat();
  }

  lcd.clear();
  lcd.setCursor(0, 0);
  
  if (currentDisplay == 0) {
    float humidity = dht.readHumidity();
    lcd.print("Room Humidity");
    lcd.setCursor(0, 1);
    lcd.print(humidity);
    lcd.print("%");
  } else if (currentDisplay == 1) {
    float temperature = dht.readTemperature();
    temperature = temperature * 9 / 5 + 32;
    lcd.print("Room Temperature");
    lcd.setCursor(0, 1);
    lcd.print(temperature);
    lcd.print(" F");
  } else {
    lcd.print(piNames[currentDisplay - 2]);
    lcd.setCursor(0, 1);
    lcd.print(cpuTemps[currentDisplay - 2]);
    lcd.print(" F");
  }

  delay(2000);
  currentDisplay = (currentDisplay + 1) % (numPIs + 2);
}
