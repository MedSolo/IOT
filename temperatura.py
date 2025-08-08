from machine import ADC

# Parametros de conversao para o sensor de temperatura
FATOR_CONVERSAO_TEMP = 3.3 / (65535)

# Sensor de Temperatura
try:
    sensor_temp_interna = ADC(4)  # ADC4  o sensor interno
    print(" Sensor Temp Interna: OK")
except Exception as e:
    print(f"L Sensor Temp Interna: {e}")
    sensor_temp_interna = None

def ler_temperatura_interna():
    """L a temperatura interna da CPU e converte para Celsius."""
    if not sensor_temp_interna:
        return None, False
    
    try:
        leitura = sensor_temp_interna.read_u16()
        voltagem = leitura * FATOR_CONVERSAO_TEMP
        temperatura = 27 - (voltagem - 0.706) / 0.001721
        
        temp_arredondada = round(temperatura, 1)
        
        return temp_arredondada, True
    except Exception as e:
        print(f"L Erro na leitura da temperatura interna: {e}")
        return None, False

# Exemplo de uso
if __name__ == "__main__":
    temp, sucesso = ler_temperatura_interna()
    if sucesso:
        print(f"A temperatura interna da CPU : {temp}C")
    else:
        print("No foi possvel ler a temperatura interna.")