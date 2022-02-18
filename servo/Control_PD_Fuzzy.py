import time
import serial
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import skfuzzy as fz
import tkinter as tk
import threading 

def grafica(distanci,tiempo):
    plt.plot(tiempo,distanci)
    plt.title('Respuesta')
    plt.xlabel('Tiempo')
    plt.ylabel('Distancia')


global Rf
Rf = 27


def vent():
    def sp1():
        global Rf
        Rf = int(texto.get())
    ventana = tk.Tk()
    ventana.geometry('190x85')
    etiqueta = tk.Label(ventana,text="Controlador Fuzzy")
    etiqueta.pack()

    boton3 = tk.Button(ventana,text="sp",command=sp1)
    texto = tk.Entry(ventana)
    texto.pack()
    boton3.pack()
    
    ventana.mainloop()


h1 = threading.Thread(target=vent)
h1.start()

uart = serial.Serial('COM11',115200)  
time.sleep(2.0) 

U    = np.arange(-38.0,38.1,0.01) 
edmn = fz.trapmf(U,[-38,-38,-28,-15])
edn  = fz.trimf(U,[-28,-15,0])
edz  = fz.trimf(U,[-15,0,15])
edp  = fz.trimf(U,[0,15,28])
edmp = fz.trapmf(U,[15,28,38,38])

W    = np.arange(-15,15.1,0.01)
demn = fz.trapmf(W,[-15,-15,-11,-7])
den  = fz.trimf(W,[-11,-7,0])
dez  = fz.trimf(W,[-7,0,7])
dep  = fz.trimf(W,[0,7,11])
demp = fz.trapmf(W,[7,11,15,15])

V   = np.arange(55,125.1,0.1)
amb = fz.trapmf(V,[55,55,67,79])
ab  = fz.trimf(V,[67,79,90])
am  = fz.trimf(V,[79,90,101])
aa  = fz.trimf(V,[90,103,115])
ama = fz.trapmf(V,[103,115,125,125])
ea  = 0
i = 0
ac_ciclo = True
vdis=[]
vtime=[]
while(ac_ciclo):
    i+=1
    uart.write(b'k')
    distancia = float(uart.readline().strip())
    e = Rf - distancia
    d = (e - ea) / 0.8 
    

    u_edmn = fz.interp_membership(U,edmn,e)
    u_edn  = fz.interp_membership(U,edn,e)
    u_edz  = fz.interp_membership(U,edz,e)
    u_edp  = fz.interp_membership(U,edp,e)
    u_edmp = fz.interp_membership(U,edmp,e)
    
    
    u_demn = fz.interp_membership(W,demn,d) 
    u_den  =  fz.interp_membership(W,den,d)
    u_dez  =  fz.interp_membership(W,dez,d)
    u_dep  =  fz.interp_membership(W,dep,d)
    u_demp = fz.interp_membership(W,demp,d)

    AND_1  = np.fmin(u_edmn,u_demn)
    AND_2  = np.fmin(u_edmn,u_den)
    AND_3  = np.fmin(u_edmn,u_dez)
    AND_4  = np.fmin(u_edmn,u_dep)
    AND_5  = np.fmin(u_edmn,u_demp)

    AND_6  = np.fmin(u_edn,u_demn) 
    AND_7  = np.fmin(u_edn,u_den)
    AND_8  = np.fmin(u_edn,u_dez)
    AND_9  = np.fmin(u_edn,u_dep)
    AND_10 = np.fmin(u_edn,u_demp)
    
    AND_11 = np.fmin(u_edz,u_demn)
    AND_12 = np.fmin(u_edz,u_den)
    AND_13 = np.fmin(u_edz,u_dez)
    AND_14 = np.fmin(u_edz,u_dep)
    AND_15 = np.fmin(u_edz,u_demp)

    AND_16 = np.fmin(u_edp,u_demn)
    AND_17 = np.fmin(u_edp,u_den)
    AND_18 = np.fmin(u_edp,u_dez)
    AND_19 = np.fmin(u_edp,u_dep)
    AND_20 = np.fmin(u_edp,u_demp)

    AND_21 = np.fmin(u_edmp,u_demn)
    AND_22 = np.fmin(u_edmp,u_den)
    AND_23 = np.fmin(u_edmp,u_dez)
    AND_24 = np.fmin(u_edmp,u_dep)
    AND_25 = np.fmin(u_edmp,u_demp)

    imp_R1  = np.fmin(AND_1,amb)
    imp_R2  = np.fmin(AND_2,amb)
    imp_R3  = np.fmin(AND_3,ab)
    imp_R4  = np.fmin(AND_4,ab)
    imp_R5  = np.fmin(AND_5,am)

    imp_R6  = np.fmin(AND_6,amb)
    imp_R7  = np.fmin(AND_7,ab)
    imp_R8  = np.fmin(AND_8,ab)
    imp_R9  = np.fmin(AND_9,am)
    imp_R10 = np.fmin(AND_10,aa)
    imp_R11 = np.fmin(AND_11,ab)
    imp_R12 = np.fmin(AND_12,ab)
    imp_R13 = np.fmin(AND_13,am)
    imp_R14 = np.fmin(AND_14,aa)
    imp_R15 = np.fmin(AND_15,aa)
    imp_R16 = np.fmin(AND_16,ab)
    imp_R17 = np.fmin(AND_17,am)
    imp_R18 = np.fmin(AND_18,aa)
    imp_R19 = np.fmin(AND_19,aa)
    imp_R20 = np.fmin(AND_20,ama)
    imp_R21 = np.fmin(AND_21,am)
    imp_R22 = np.fmin(AND_22,aa)
    imp_R23 = np.fmin(AND_23,aa)
    imp_R24 = np.fmin(AND_24,ama)
    imp_R25 = np.fmin(AND_25,ama)


    agre1 = np.fmax(imp_R1,imp_R2,imp_R6)#amb

    agre2_1= np.fmax(imp_R3,imp_R4,imp_R7)
    agre2_2 = np.fmax(imp_R8,imp_R11,imp_R12)
    agre2 = np.fmax(agre2_1,agre2_2,imp_R16)#ab

    agre3_1 = np.fmax(imp_R5,imp_R9,imp_R13)
    agre3 = np.fmax(agre3_1,imp_R17,imp_R21)#am

    agre4_1 = np.fmax(imp_R10,imp_R14,imp_R15)
    agre4_2 = np.fmax(imp_R18,imp_R19,imp_R23)
    agre4 = np.fmax(agre4_1,agre4_2,imp_R22)#aa

    agre5 = np.fmax(imp_R20,imp_R24,imp_R25)#ama

    agregacion = agre1 + agre2 + agre3 + agre4 + agre5

    defuzzi_out = fz.defuzz(V,agregacion,'SOM')
    u_defuzzi_out = fz.interp_membership(V,agregacion,defuzzi_out)
    uart.write(b's')
    uart.write(str(defuzzi_out).encode())
    #print(defuzzi_out)
    ea = e
    vdis.append(distancia)
    vtime.append(i)
    print(f'Dostancia: {distancia}  Error: {e}')

    '''axes = plt.gca()
    axes.set_xlim(56,125.8)
    axes.set_ylim(-0.1,1.1)
    plt.title(r'$\mathbf{Conjunto \ Difuso \ DCout}$',fontsize=12,color='0.6')
    plt.xlabel(r'$\mathbf{V}=[0, 100]$',fontsize=14,color='g')
    plt.ylabel(r'$\mathbf{\mu_{DCout}(x)}$',fontsize=14,color='g')
    plt.text(90,1.03,r'$\mathbf{Rf} = %.2f $, ' % Rf,fontsize=12,color='b')
    plt.text(56,1.03,r'$\mathbf{distancia} = %.2f $, ' % distancia,fontsize=12,color='b')
    plt.text(70,1.03,r'$\mathbf{e} = %.2f $, ' % e,fontsize=12,color='b')
    plt.text(defuzzi_out - 13.25, -0.07525, r'$\mathbf{angulo}= %.2f $, ' % defuzzi_out,fontsize=12,color='k')
    plt.plot(V,agregacion,'orange',[defuzzi_out,defuzzi_out],[0,u_defuzzi_out],'k',linewidth=2.5,alpha=0.9)
    plt.grid()
    plt.draw()
    plt.pause(1e-17)
    plt.clf()'''
grafica(vdis,vtime)



