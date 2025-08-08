from machine import Pin, ADC

# Calibrao do sensor de solo (ajuste esses valores para o seu sensor)
SOLO_SECO = 45000  # Valor quando o sensor est completamente seco
SOLO_UMIDO = 20000 # Valor quando o sensor est na gua

# Inicializao do sensor de solo no pino 28
try:
    adc_solo = ADC(Pin(28))
    print("Sensor Solo: OK")
except Exception as e:
    print(f"L Sensor Solo: {e}")
    adc_solo = None
    exit()

def ler_sensor_solo():
    """L o valor do sensor de solo e converte para porcentagem."""
    if not adc_solo:
        print("L Sensor de solo no inicializado.")
        return None, None, False
        
    try:
        valor_raw = adc_solo.read_u16()
        
        if valor_raw >= SOLO_SECO:
            porcentagem = 0
        elif valor_raw <= SOLO_UMIDO:
            porcentagem = 100
        else:
            range_total = SOLO_SECO - SOLO_UMIDO
            diferenca = SOLO_SECO - valor_raw
            porcentagem = int((diferenca * 100) / range_total)
            porcentagem = max(0, min(100, porcentagem))
            
        return valor_raw, porcentagem, True
    except Exception as e:
        print(f"L Erro no sensor de solo: {e}")
        return None, None, False

# Exemplo de como usar a funo
if __name__ == "__main__":
    while True:
        valor_raw, porcentagem, sucesso = ler_sensor_solo()
        if sucesso:
            print(f"Valor bruto: {valor_raw}, Umidade do solo: {porcentagem}%")
        else:
            print("Falha na leitura do sensor de solo.")
        time.sleep(5)  # Aguarda 5 segundos antes de uma nova leitura