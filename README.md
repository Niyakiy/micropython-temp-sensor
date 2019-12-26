# Micropython Temperature Sensor

## Ingredients

* NodeMCU ESP8266 based board
* BME280 multisensor
* AM2301 multisensor

## Steps to prepare 
* DHT (AM2301) sensor's data line connected to `GPIO0` (`D3`) line
* BME sensor's SDA connected to `GPIO4` (`D2`) line and SCL is connected to `GPIO5` (`D1`) line
* Both sensors connected to `3.3V` and `Gnd` lines on NodeMCU
* Special file `wifi-credentials.txt` should contain WiFi SSID in 1st line and its password on 2nd
