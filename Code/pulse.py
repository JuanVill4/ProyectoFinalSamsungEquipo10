from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106
from PIL import ImageFont
import sys
from pathlib import Path
import time
# Agrega la carpeta Oxigen al sys.path
oxigen_path = Path(__file__).resolve().parent / 'Oxigen'
sys.path.append(str(oxigen_path))
from hrmonitor import HeartRateMonitor
# Inicialización del bus I2C y dirección del dispositivo OLED
serial = i2c(port=1, address=0x3C)

# Inicialización del dispositivo OLED con el controlador SH1106
device = sh1106(serial, rotate=0)

font_path = "ProyectoFinalSamsungEquipo10/Code/templates/ALBA____.TTF"
font = ImageFont.truetype(font_path, 18)
with canvas(device) as draw:
        ancho_texto, alto_texto = draw.textsize("Pulsioximetro", font=font)
        ancho_display, alto_display = device.width, device.height
        x = (ancho_display - ancho_texto) / 2

        ancho_texto1, alto_texto1 = draw.textsize("Dedo no detectado")
        x1 = (ancho_display - ancho_texto1) / 2




def display_sensor_data(hrm):
    with canvas(device) as draw:
        draw.text((x, 0), "Pulsioxímetro", font=font, fill="white")
        if hrm.bpm > 0:      
            draw.text((10, 25), f"Heart Rate: {int(hrm.bpm)} BPM",fill="white")
            draw.text((10, 40), f"SpO2: {int(hrm.spo2)}%",fill="white")
        if hrm.bpm == 0:
            draw.text((x1, 35), "Dedo no detectado",fill="white")

def monitor_heart_rate_and_spo2():
    hrm = HeartRateMonitor(print_raw=False, print_result=False)
    hrm.start_sensor()

    try:
        print("Monitoreo de la frecuencia cardíaca y oxigenación iniciado. Presiona CTRL+C para detener.")
        while True:
            display_sensor_data(hrm)
            time.sleep(0.5)  # Espera un segundo antes de leer el siguiente valor
    except KeyboardInterrupt:
        print("Deteniendo el monitoreo...")
    finally:
        hrm.stop_sensor()
 
 
if __name__ == "__main__":
    monitor_heart_rate_and_spo2()