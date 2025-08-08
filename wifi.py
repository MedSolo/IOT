import network
import time

WIFI_SSID = "SSID"
WIFI_SENHA = "PASSWORD"
SERVER_URL = "http://SEU_IP/dados"

def conectar_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if wlan.isconnected():
        print(" WiFi ja conectado!")
        return True
    
    print("= Conectando WiFi...")
    wlan.connect(WIFI_SSID, WIFI_SENHA)
    
    timeout = 15
    while not wlan.isconnected() and timeout > 0:
        time.sleep(1)
        timeout -= 1
    
    if wlan.isconnected():
        print(" WiFi conectado com sucesso!")
        print(" Endereco IP:", wlan.ifconfig()[0])
    else:
        print(" Falha na conexao WiFi.")
        
    return wlan.isconnected()