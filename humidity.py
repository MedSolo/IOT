import dht
import machine

class HumiditySensor:
    def __init__(self, pin):
        self.pin = machine.Pin(pin)
        self.sensor = dht.DHT11(self.pin)
        self.last_humidity = None

    def read(self):
        try:
            self.sensor.measure()
            self.last_humidity = self.sensor.humidity()
            return self.last_humidity
        except Exception as e:
            print("Erro ao ler umidade:", e)
            return None

    def get_last_reading(self):
        return self.last_humidity