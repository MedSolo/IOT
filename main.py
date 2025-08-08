import urequests
import json
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

# --- IMPORTACAO DOS MODULOS ---
from temperatura import ler_temperatura_interna
from umidade_solo import ler_sensor_solo
import wifi 
from wifi import conectar_wifi 

print("<1 MedSolo")
print("="*40)

i2c = I2C(1, scl=Pin(15), sda=Pin(14))
try:
    oled = SSD1306_I2C(128, 64, i2c)
    oled.fill(0)
    oled.text("MedSolo Iniciando", 0, 0)
    oled.show()
    print(" Display: OK")
except Exception as e:
    print(f"L Display: {e}")
    oled = None

def enviar_dados(temp, solo_pct):
    """Envia dados de temperatura e umidade do solo para o servidor."""
    try:
        dados = {
            "temperatura": temp,
            "solo": solo_pct
        }
        resposta = urequests.post(
            wifi.SERVER_URL,
            data=json.dumps(dados),
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        sucesso = resposta.status_code == 200
        resposta.close()
        if sucesso:
            print(" Dados enviados")
        else:
            print(f"L Erro servidor: {resposta.status_code}")
        return sucesso
    except Exception as e:
        print(f"L Erro envio: {e}")
        return False

def atualizar_display(temp, solo_pct, wifi_ok, server_ok, ciclo):
    """Atualiza o display OLED com os dados dos sensores e status da conexao."""
    if not oled:
        return
    try:
        oled.fill(0)
        oled.text("=== MedSolo ===", 0, 0)
        oled.text(f"Temp: {temp}C", 0, 16)
        oled.text(f"Solo: {solo_pct}%", 0, 32)
        if wifi_ok and server_ok:
            status = "Online"
        elif wifi_ok:
            status = "WiFi OK"
        else:
            status = "Offline"
        oled.text(f"Status: {status}", 0, 48)
        oled.text(f"Ciclo: {ciclo}", 0, 56)
        oled.show()
    except Exception as e:
        print(f"L Erro display: {e}")

# --- Funcao Principal ---
def main():
    print("= Iniciando monitoramento...")
    wifi_conectado = conectar_wifi()
    if not wifi_conectado:
        print("L WiFi falhou - Verifique as credenciais e o roteador.")
    ciclo = 0
    print("\n= Pressione Ctrl+C para parar\n")
    try:
        while True:
            ciclo += 1
            print(f"--- Ciclo {ciclo} ---")
            
            solo_raw, solo_pct, solo_ok = ler_sensor_solo()
            temp, temp_ok = ler_temperatura_interna()
            
            if solo_ok and temp_ok:
                server_ok = False
                if wifi_conectado:
                    server_ok = enviar_dados(temp, solo_pct)
                
                atualizar_display(temp, solo_pct, wifi_conectado, server_ok, ciclo)
                print(f"= Temp: {temp}C | Solo: {solo_pct}% | Servidor: {'OK' if server_ok else 'L'}")
            else:
                print("L Falha na leitura dos sensores.")
                if oled:
                    oled.fill(0)
                    oled.text("ERRO SENSOR", 0, 20)
                    oled.show()
            
            print(" Aguardando 10s...\n")
            time.sleep(10)
            
    except KeyboardInterrupt:
        print("\n= Programa parado")
        if oled:
            oled.fill(0)
            oled.text("PROGRAMA", 0, 20)
            oled.text("PARADO", 0, 32)
            oled.show()

if __name__ == "__main__":
    try:
        resposta = input("Iniciar monitoramento? (S/N): ").lower().strip()
        if resposta in ['s', 'sim', 'y', 'yes']:
            main()
        else:
            print("=K Programa encerrado")
    except:
        print("=K Programa encerrado")