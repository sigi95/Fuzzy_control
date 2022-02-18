import tkinter as tk
import threading 
import time
import serial
import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fz

global Rf
Rf = 10
global ac_ciclo
ac_ciclo = True

vdis=[]
vtime=[]
vsp=[]
vsc = []
def grafica(distanci,tiempo,sp,control):
    
    plt.plot(distanci,tiempo,label="Distancia")
    plt.plot(sp,label="Set point")
    plt.plot(control,label="Señal de control")
    plt.title('Respuesta')
    plt.xlabel('Tiempo')
    plt.ylabel('Distancia')
    plt.legend(loc=1)
    plt.grid(True)
    plt.show()
 
def vent():
    def sp1():
        global Rf
        Rf = int(texto.get())
    

    def desactivar():
        global ac_ciclo
        ac_ciclo = False

    
    ventana = tk.Tk()
    ventana.geometry('190x85')
    etiqueta = tk.Label(ventana,text="Controlador Fuzzy")
    etiqueta.pack()

    setp = tk.Button(ventana,text="sp",command=sp1)
    desac = tk.Button(ventana,text="Desactivar",command=desactivar)
    texto = tk.Entry(ventana)
    texto.pack()
    setp.pack()
    desac.pack()
    
    ventana.mainloop()


h1 = threading.Thread(target=vent)
h1.start()

uart = serial.Serial('COM7',115200)
time.sleep(2.0) 

U    = np.arange(-38.0,38.1,0.01) 
edn = fz.trapmf(U,[-38,-38,-14,0])
edz  = fz.trimf(U, [-14,0,14])
edp = fz.trapmf(U,[0,14,38,38])

W = np.arange(-15,15.1,0.01)
den = fz.trapmf(W, [-15,-15,-5,0])
dez = fz.trimf(W, [-5,0,5])
dep = fz.trapmf(W, [0,5,15,15])

V = np.arange(55,125.1,0.1)
ab = fz.trapmf(V,[55,55,75,90])
am  = fz.trimf(V,[75,90,105])
aa = fz.trapmf(V,[90,105,125,125])

ea = 0
i = 0


while ac_ciclo:
    i+=1
    uart.write(b'k')
    distancia = float(uart.readline())
    e = Rf - distancia 
    d = (e - ea)/0.8

    u_edn  = fz.interp_membership(U,edn,e)
    u_edz  = fz.interp_membership(U,edz,e)
    u_edp  = fz.interp_membership(U,edp,e)
    
    
    u_den =  fz.interp_membership(W,den,d)
    u_dez =  fz.interp_membership(W,dez,d)
    u_dep =  fz.interp_membership(W,dep,d)
    

    AND_1 = np.fmin(u_edn,u_den)
    AND_2 = np.fmin(u_edn,u_dez)
    AND_3 = np.fmin(u_edn,u_dep)

    AND_4 = np.fmin(u_edz,u_den)
    AND_5 = np.fmin(u_edz,u_dez)
    AND_6 = np.fmin(u_edz,u_dep)

    AND_7 = np.fmin(u_edp,u_den)
    AND_8 = np.fmin(u_edp,u_dez)
    AND_9 = np.fmin(u_edp,u_dep)

    imp_R1 = np.fmin(AND_1,ab)
    imp_R2 = np.fmin(AND_2,ab)
    imp_R3 = np.fmin(AND_3,am)
    imp_R4 = np.fmin(AND_4,ab)
    imp_R5 = np.fmin(AND_5,am)
    imp_R6 = np.fmin(AND_6,aa)
    imp_R7 = np.fmin(AND_7,am)
    imp_R8 = np.fmin(AND_8,aa)
    imp_R9 = np.fmin(AND_9,aa)
  
    agre_1 = np.fmax(imp_R1,imp_R2,imp_R4)
    agre_2 = np.fmax(imp_R3,imp_R5,imp_R7)
    agre_3 = np.fmax(imp_R6,imp_R8,imp_R9)

    agre = agre_1 + agre_2 + agre_3

    defuzzi_out = fz.defuzz(V,agre,'SOM')
    uart.write(b's')
    uart.write(str(defuzzi_out).encode())
    vdis.append(distancia)
    vtime.append(i)
    vsp.append(Rf)
    vsc.append(defuzzi_out)
    print(f'Dostancia: {distancia}  Error: {e}')
    ea = e

grafica(vtime,vdis,vsp,vsc)