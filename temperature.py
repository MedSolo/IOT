import dht
import machine

class TemperatureSensor:
    def __init__(self, pin):
        self.pin = machine.Pin(pin)
        self.sensor = dht.DHT11(self.pin)
        self.last_temperature = None

    def read(self):
        try:
            self.sensor.measure()
            self.last_temperature = self.sensor.temperature()
            return self.last_temperature
        except Exception as e:
            print("Erro ao ler temperatura:", e)
            return None

    def get_last_reading(self):
        return self.last_temperature