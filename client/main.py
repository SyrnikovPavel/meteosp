print("Hello from ESP32")

from machine import Pin, I2C
from time import sleep
from wifi import connect_network
import urequests
import ujson
import bme
import ssd1306
import max44009

# Соединение с Wi-Fi
wi_fi_status = connect_network()

# I2C Иницилизация
i2c_bme = I2C(scl=Pin(22), sda=Pin(21), freq=10000)
i2c_oled = I2C(-1, scl=Pin(17), sda=Pin(16))
i2c_lux = I2C(scl=Pin(4), sda=Pin(0))

# Иницилизация экрана
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c_oled)

# Иницилизация датчика BME280
bme_c = bme.BME280(i2c=i2c_bme)

# Иницилизация датчика GY-49
luxometer = max44009.MAX44009(i2c=i2c_lux)

n = 0
while True:

    # Чистка экрана
    oled.fill(0)

    # Получение данных с датчиков
    temp = round(float(bme_c.temperature), 2)
    hum = round(float(bme_c.humidity), 2)
    pres = round(bme_c.pressure * 0.75, 2)
    lux = round(float(luxometer.illuminance_lux), 2)

    # Вывод на экран
    oled.text('Temp: {0}'.format(temp), 0, 10)
    oled.text('Hum:  {0}'.format(hum), 0, 20)
    oled.text('Pres: {0}'.format(pres), 0, 30)
    oled.text('Lux:  {0}'.format(lux), 0, 40)
    if wi_fi_status:
        oled.text('Wi-Fi: True', 0, 50)
    oled.show()

    # TODO Добавить отправку результатов

    # Сон
    sleep(5)

    n += 1

    if n == 12:
        data = {'temp': temp, 'hum': hum, 'pres': pres, 'lux': lux}
        res = urequests.request('POST', 'http://syrnikovpavel.pythonanywhere.com/climat_save', json=ujson.dumps(data))
        n = 0
