import network
import time

class WiFiConnection:
    def __init__(self, ssid, password):
        self.ssid = ssid
        self.password = password
        self.sta_if = network.WLAN(network.STA_IF)
        self.connected = False

    # Conecta à rede Wi-Fi
    def connect(self):
        if not self.sta_if.isconnected():
            print("Conectando ao Wi-Fi...")
            self.sta_if.active(True)
            self.sta_if.connect(self.ssid, self.password)

            for _ in range(15):  
                if self.sta_if.isconnected():
                    self.connected = True
                    print("Conectado ao Wi-Fi! IP:", self.sta_if.ifconfig()[0])
                    return True
                time.sleep(1)

            print("Falha ao conectar ao Wi-Fi.")
            self.connected = False
            return False
        return True

    # Verifica se está conectado
    def is_connected(self):
        return self.sta_if.isconnected()

    # Retorna o IP atual
    def get_ip(self):
        return self.sta_if.ifconfig()[0] if self.is_connected() else None