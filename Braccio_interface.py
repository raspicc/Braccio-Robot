import tkinter as tk
import pyvisa
import time
from time import sleep
from tkinter import *
from PIL import Image, ImageTk
import tkinter.filedialog as tkFileDialog
from tkinter import Tk, filedialog

rm = pyvisa.ResourceManager()

# Identificador del dispositivo de medición que nos interesa
device_id = 'Hcal ,Braccio Instrument ,#00,v1.0.0'

# Busca el dispositivo de medición en todas las direcciones VISA disponibles
resources = rm.list_resources()
for resource in resources:
    try:
        inst = rm.open_resource(resource, timeout=None)
        inst.write_termination = "\n"
        inst.read_termination = "\n"
        time.sleep(2)
        idn = inst.query('*IDN?')
        if idn.strip() == device_id:
            print('Conectado al dispositivo con identificador', device_id, 'en la dirección VISA', resource)
            break
        else:
            inst.close()
    except pyvisa.VisaIOError:
        pass

posiciones = []

def show_values(event):
    delay = 20
    base = base_slider.get()
    hombro = hombro_slider.get()
    codo = codo_slider.get()
    muneca_v = muneca_v_slider.get()
    muneca_r = muneca_r_slider.get()
    pinza = pinza_slider.get()
    inst.write("Braccio0 {} {} {} {} {} {} {}".format(delay, base, hombro, codo, muneca_v, muneca_r, pinza))

def guardar_posicion():
    delay = 20
    base = base_slider.get()
    hombro = hombro_slider.get()
    codo = codo_slider.get()
    muneca_v = muneca_v_slider.get()
    muneca_r = muneca_r_slider.get()
    pinza = pinza_slider.get()
    posiciones.append((delay, base, hombro, codo, muneca_v, muneca_r, pinza))
    print("Posición guardada:", posiciones[-1])

def reset_posiciones():
    global posiciones
    posiciones = []
    print("Posiciones reiniciadas.")

def reproducir_movimiento():
    global posiciones
    if len(posiciones) > 0:
        for posicion in posiciones:
            inst.write("Braccio0 {} {} {} {} {} {} {}".format(*posicion))
            time.sleep(2)
    else:
        print("No se han guardado posiciones.")


def guardar():
    filename = tk.filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if filename:
        with open(filename, 'w') as file:
            for pos in posiciones:
                file.write("{},{},{},{},{},{},{}\n".format(*pos))
            print("Archivo guardado con éxito:", filename)

def abrir():
    global posiciones
    filename = tk.filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if filename:
        with open(filename, 'r') as file:
            posiciones = [tuple(map(int, line.strip().split(','))) for line in file]
        print("Archivo cargado con éxito:", filename)


root = tk.Tk()
root.title("Braccio Interface - LACH 2023")
root.geometry("350x450")
root.resizable(width=False, height=False)


menu_bar = tk.Menu(root)
root.config(menu=menu_bar)
root.configure(bg='white')

# Crear el menú "Archivo"
archivo_menu = tk.Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label="Archivo", menu=archivo_menu)

# Agregar las opciones al menú "Archivo"

archivo_menu.add_command(label="Abrir", command=abrir)


archivo_menu.add_command(label="Guardar", command=guardar)
archivo_menu.add_separator()
archivo_menu.add_command(label="Salir", command=root.destroy)


pinza_slider = tk.Scale(root, from_=10, to=73, orient=tk.HORIZONTAL, label="Pinza", length=300,activebackground='#ff7c39')
muneca_r_slider = tk.Scale(root, from_=55, to=125, orient=tk.HORIZONTAL, label="Muñeca rotación", length=300,activebackground='#ff7c39')
muneca_v_slider = tk.Scale(root, from_=45, to=135, orient=tk.HORIZONTAL, label="Muñeca vertical", length=300,activebackground='#ff7c39')
codo_slider = tk.Scale(root, from_=45, to=135, orient=tk.HORIZONTAL, label="Codo", length=300,activebackground='#ff7c39')
hombro_slider = tk.Scale(root, from_=45, to=135, orient=tk.HORIZONTAL, label="Hombro", length=300,activebackground='#ff7c39') # 15 165
base_slider = tk.Scale(root, from_=0, to=180, orient=tk.HORIZONTAL, label="Base", length=300,activebackground='#ff7c39')


base_slider.set(0)
hombro_slider.set(45)
codo_slider.set(135)
muneca_v_slider.set(45)
muneca_r_slider.set(135)
pinza_slider.set(10)


pinza_slider.pack()
muneca_r_slider.pack()
muneca_v_slider.pack()
codo_slider.pack()
hombro_slider.pack()
base_slider.pack()

guardar_posicion_inicial_button = tk.Button(root, text="Guardar posición", command=guardar_posicion)
guardar_posicion_inicial_button.pack()

guardar_posicion_final_button = tk.Button(root, text="Reset posiciones", command=reset_posiciones)
guardar_posicion_final_button.pack()

reproducir_movimiento_button = tk.Button(root, text="Reproducir movimiento", command=reproducir_movimiento,bg='#ff7c39', fg='white')
reproducir_movimiento_button.pack()

base_slider.bind("<ButtonRelease>", show_values)
hombro_slider.bind("<ButtonRelease>", show_values)
codo_slider.bind("<ButtonRelease>", show_values)
muneca_v_slider.bind("<ButtonRelease>", show_values)
muneca_r_slider.bind("<ButtonRelease>", show_values)
pinza_slider.bind("<ButtonRelease>", show_values)

root.title("Braccio Interface - LACH 2023")
root.mainloop()
