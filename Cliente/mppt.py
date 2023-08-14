import matplotlib.pyplot as plt
import numpy as np
import sys
import lector

lector = lector.Lector()

# Chekeo los argumentos que se pasaron por linea de comando
if len(sys.argv) > 2:
  print(f"Cantidad invalida de argumentos. Solo admite enviar el puerto. DEFAULT: COM4")
  quit()

try:
  if len(sys.argv) == 2:
    serial_port = str(sys.argv[1])
    if not serial_port.startswith("COM"):
      print(f"Nombre del puerto invalido. Utilice COMx.")
      quit()

    lector.setPort(serial_port)
except Exception as e:
  print(f"Error al abrir el puerto serie. Compruebe la configuracion del sistema.\n{e}")
  quit()

# Variable para marcar la finalizacion del bucle principal
plot_close_event = 0

# Handler para manejar el cierre de la ventana
def handle_close(evt):
	global plot_close_event
	plot_close_event = 1

# Tamaño del eje horizontal del grafico
size = 100

# Variables que almacenan los datos para mostrar, x_vec es fija, las demas se actualizan a medida que llega informacion
x_vec = np.linspace(0,1,size+1)[0:-1]
duty_buck1 = np.zeros(len(x_vec))
duty_buck2 = np.zeros(len(x_vec))
tension_in = np.zeros(len(x_vec))
tension_med = np.zeros(len(x_vec))
tension_out = np.zeros(len(x_vec))
potencia_panel = np.zeros(len(x_vec))
potencia_salida = np.zeros(len(x_vec))

# Configuro el plot
plt.ion()
fig = plt.figure(figsize=(12,8))
fig.canvas.mpl_connect('close_event', handle_close)
fig.canvas.manager.set_window_title('MPPT - Electronica de Potencia - UTN FRBA')
plt.suptitle('Datos de MPPT')

# Agrego un subplot para los dutys
axis_duty = fig.add_subplot(311)                        
line_duty_buck1, = axis_duty.plot(x_vec, duty_buck1, "r", label="Duty Buck 1")
line_duty_buck2, = axis_duty.plot(x_vec, duty_buck2, "b", label="Duty Buck 2")
axis_duty.set_ylim([0,1])
plt.grid()
plt.legend(loc='upper right')

# Agrego un subplot para las tensiones
axis_tension = fig.add_subplot(312)                        
line_tension_in, = axis_tension.plot(x_vec, tension_in, "r", label="Tension Entrada")
line_tension_med, = axis_tension.plot(x_vec, tension_med, "g", label="Tension Intermedia")
line_tension_out, = axis_tension.plot(x_vec, tension_out, "b", label="Tension Salida")
plt.grid()
plt.legend(loc='upper right')

# Agrego un subplot para las potencias
axis_potencia = fig.add_subplot(313)                        
line_potencia_panel, = axis_potencia.plot(x_vec, potencia_panel, "r", label="Potencia Panel")
line_potencia_salida, = axis_potencia.plot(x_vec, potencia_salida, "b", label="Potencia Salida")
plt.grid()
plt.legend(loc='upper right')


while plot_close_event==0:
  if lector.hayDatos():

    # Leo un dato
    data = lector.leer()

    # Si vino en false es porque no tengo datos, busco el proximo
    if data == False:
       continue
    
    # Agrego los datos a los buffers
    duty_buck1 = np.append(duty_buck1[1:], data["d1"])
    duty_buck2 = np.append(duty_buck2[1:], data["d2"])

    # Agrego los datos a los buffers
    tension_in = np.append(tension_in[1:], data["vin"])
    tension_med = np.append(tension_med[1:], data["vmed"])
    tension_out = np.append(tension_out[1:], data["vout"])

    # Agrego los datos a los buffers
    potencia_panel = np.append(potencia_panel[1:], data["vin"]*data["cin"])
    potencia_salida = np.append(potencia_salida[1:], data["vout"]*data["cout"])

    # Actualizo las lineas en el grafico
    line_duty_buck1.set_ydata(duty_buck1)
    line_duty_buck2.set_ydata(duty_buck2)

    line_tension_in.set_ydata(tension_in)
    line_tension_med.set_ydata(tension_med)
    line_tension_out.set_ydata(tension_out)

    line_potencia_panel.set_ydata(potencia_panel)
    line_potencia_salida.set_ydata(potencia_salida)

    # Actualizo los limites en el grafico
    minimo = np.min([tension_in, tension_med, tension_out])
    maximo = np.max([tension_in, tension_med, tension_out])
    if maximo>=line_tension_in.axes.get_ylim()[1] or maximo<line_tension_in.axes.get_ylim()[1]-2:
      axis_tension.set_ylim([0,maximo+1])

    # Actualizo los limites en el grafico
    minimo = np.min([potencia_panel, potencia_salida])
    maximo = np.max([potencia_panel, potencia_salida])
    if maximo>=line_potencia_panel.axes.get_ylim()[1] or maximo<line_potencia_panel.axes.get_ylim()[1]-2:
      axis_potencia.set_ylim([0,maximo+1])

  plt.pause(0.1)