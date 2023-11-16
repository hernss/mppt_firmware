import serial
import json

class Lector:
  def __init__(self):
    self.port = "COM16"
    self.speed = 9600
    self.serial = False
    try:  
      self.serial = serial.Serial(self.port, self.speed,timeout=1)
    except:
      print("[__init__] Error al abrir el puerto")

  def setPort(self, port = "COM16", speed = 9600):
    self.port = port
    self.speed = speed
    try:
      if self.serial != False and self.serial.is_open:
        self.serial.close()
        self.serial = serial.Serial(self.port, self.speed,timeout=1)
    except:
      print("[setPort] Error al abrir el puerto")

  def openPort(self):
    try:
      if self.serial != False and self.serial.is_open:
        self.serial.close()

      self.serial = serial.Serial(self.port, self.speed,timeout=1)
      self.serial.open()
    except:
      print("[openPort] Error al abrir el puerto")

  def closePort(self):
    try:
      if self.serial != False and self.serial.is_open:
        self.serial.close()
    except:
      print("[closePort] Error al cerrar el puerto")

  def resetData(self):
    # Limpio el buffer del puerto serie
    self.serial.reset_input_buffer()
    self.serial.reset_output_buffer()
  
  def hayDatos(self):
    #return True
    if self.serial == False or not self.serial.is_open:
      return False
    
    return self.serial.in_waiting > 0

  def leer(self):
    testData = '{ "vin":17450, "vmed":12450, "vout":4200, "cin":570, "cout":2140, "d1":240, "d2":640 }'
    #j =  json.loads(testData)
    #for k in j.keys():
    #    j[k] /= 1000.0
    #return j

    if self.serial != False and not self.serial.is_open:
      return False
    
    data = ""
    try:
      data = self.serial.readline().decode('utf-8').rstrip()
    except:
      print("[leer] Error al leer el puerto")
      return False
    
    try:
      print (data)
      j =  json.loads(data)
      # Convierto todos los campos de int a float usando los ultimos tres digitos como decimales
      for k in j.keys():
        j[k] /= 1000.0
      return j
    except:
      print("[leer] Error al decodificar el JSON")
      return False