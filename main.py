import time
import json
import machine
import urequests as requests
from wifi_connection import WiFiConnection
from temperature_sensor import TemperatureSensor
from humidity_sensor import HumiditySensor

# CONFIGURAÇÕES
WIFI_SSID = # rede wifi
WIFI_PASSWORD = # senha
BACKEND_URL = # api back
DEVICE_ID = "BITDOG-01"
SENSOR_PIN = 4
UPDATE_INTERVAL = 30 

# INICIALIZAÇÃO DOS COMPONENTES
wifi = WiFiConnection(WIFI_SSID, WIFI_PASSWORD)
temp_sensor = TemperatureSensor(SENSOR_PIN)
hum_sensor = HumiditySensor(SENSOR_PIN)

# FUNÇÃO PARA ENVIAR DADOS AO BACKEND
def send_to_backend(temperature, humidity):
    payload = {
        "device_id": DEVICE_ID,
        "temperature": temperature,
        "humidity": humidity,
        "timestamp": time.time()  
    }

    headers = {"Content-Type": "application/json"}

    try:
        print("Enviando dados para o backend...")
        response = requests.post(BACKEND_URL, data=json.dumps(payload), headers=headers)
        print("Resposta:", response.status_code, response.text)
        response.close()
        return response.status_code == 200
    except Exception as e:
        print("Erro ao enviar dados:", e)
        return False

def main():
    last_sent = 0

    while True:
        wifi_c = wifi.connect()

        if not wifi_c:
            print("Wi-Fi desconectado. Tentando novamente...")
            time.sleep(5)
            continue

        # Leitura dos sensores
        temperature = temp_sensor.read()
        humidity = hum_sensor.read()

        if temperature is not None and humidity is not None:
            print(f"Leitura atual: Temp={temperature}°C | Hum={humidity}%")
        else:
            temperature = temp_sensor.get_last_reading()
            humidity = hum_sensor.get_last_reading()
            if temperature is not None and humidity is not None:
                print(f"Usando última leitura válida: Temp={temperature}°C | Hum={humidity}%")
            else:
                print("Erro na leitura dos sensores.")
                time.sleep(5)
                continue

        # Enviar dados a cada intervalo
        current_time = time.time()
        if current_time - last_sent > UPDATE_INTERVAL:
            if send_to_backend(temperature, humidity):
                print("Dados enviados com sucesso.")
                last_sent = current_time
            else:
                print("Erro no envio dos dados.")

        time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Erro fatal:", e)
        time.sleep(10)
        machine.reset()
