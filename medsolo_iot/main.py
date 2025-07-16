from machine import Pin, I2C
import time
import dht
import network
import urequests

# Sensor DHT11 no pino 4
sensor = dht.DHT11(Pin(4))

# Conecta ao Wi-Fi
def conecta_wifi(ssid, senha):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, senha)
    while not wlan.isconnected():
        time.sleep(1)
    print("Conectado! IP:", wlan.ifconfig()[0])

# Inicializa Wi-Fi
conecta_wifi("Gabriel", "16081914")

# Loop principal: envia leitura do sensor
while True:
    try:
        sensor.measure()
        temp = sensor.temperature()
        umid = sensor.humidity()

        print("Enviando dados:", temp, umid)

        payload = {
            "temperatura": temp,
            "umidade": umid
        }

        resposta = urequests.post(
            "http://192.168.3.103:3000/dados", 
            json=payload
        )

        print("Resposta:", resposta.status_code)
        resposta.close()

    except Exception as e:
        print("Erro:", e)

    time.sleep(5)
