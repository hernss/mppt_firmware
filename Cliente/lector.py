import serial
import json

class Lector:
  def __init__(self):
    self.port = "COM4"
    self.speed = 115200
    self.serial = False
    try:  
      self.serial = serial.Serial(self.port, self.speed)
    except:
      print("Error al abrir el puerto")

  def setPort(self, port = "COM4", speed = 115200):
    self.port = port
    self.speed = speed
    try:
      if self.serial != False and self.serial.is_open:
        self.serial.close()
    except:
      print("Error al abrir el puerto")

  def openPort(self):
    try:
      if self.serial != False and self.serial.is_open:
        self.serial.close()

      self.serial.open()
    except:
      print("Error al abrir el puerto")

  def closePort(self):
    try:
      if self.serial != False and self.serial.is_open:
        self.serial.close()
    except:
      print("Error al cerrar el puerto")

  def resetData(self):
    # Limpio el buffer del puerto serie
    self.serial.reset_input_buffer()
    self.serial.reset_output_buffer()
  
  def hayDatos(self):
    if self.serial == False or not self.serial.is_open:
      return False
    
    return self.serial.in_waiting > 0

  def leer(self):
    testData = '{ "vin":1745, "vmed":1245, "vout":420, "cin":57, "cout":214, "d1":24, "d2":64 }'
    #j =  json.loads(testData)
    #for k in j.keys():
    #    j[k] /= 100.0
    #return j

    if self.serial != False and not self.serial.is_open:
      return False
    
    data = ""
    try:
      data = self.serial.readline().decode('utf-8').rstrip()
    except:
      print("Error al leer el puerto")
      return False
    
    try:
      j =  json.loads(data)
      # Convierto todos los campos de int a float usando los ultimos dos digitos como decimales
      for k in j.keys():
        j[k] /= 100.0
      return j
    except:
      print("Error al leer el puerto")
      return False