import tkinter as tk
from tkcalendar import Calendar,DateEntry
import requests
import pandas as pd
from datetime import datetime
from datetime import date
from datetime import timedelta

def consulta():

    try:
        consultas_terminadas=0
        boton_calculo["state"]='disabled'
        lista_sistemas = []
        lista_procesos = []
        if check_sin.get() == 1:
            lista_sistemas.append("SIN")
        if check_bca.get() == 1:
            lista_sistemas.append("BCA")
        if check_bcs.get() == 1:
            lista_sistemas.append("BCS")
        if check_mda.get() == 1:
            lista_procesos.append("MDA")
        if check_mtr.get() == 1:
            lista_procesos.append("MTR")
        fecha_ini = cal1.get_date()
        fecha_fin = cal2.get_date()

        delta = fecha_fin - fecha_ini
        delta = delta.days

        mod_fecha = delta % 7 
        div_fecha = delta // 7 

        lista_fechas_inicio=[]
        lista_fechas_final=[]
        lista_fechas_inicio.append(fecha_ini)
        for i in range(div_fecha):    
            lista_fechas_final.append(lista_fechas_inicio[-1]+timedelta(days=6))
            lista_fechas_inicio.append(lista_fechas_inicio[-1]+timedelta(days=7))
        if mod_fecha != 0:
            lista_fechas_final.append(fecha_fin) 
        if fecha_ini == fecha_fin:
            lista_fechas_final.append(fecha_fin)

        appended_data_list = []
        for sistema in lista_sistemas:
            for proceso in lista_procesos:
                for i in range(0,len(lista_fechas_final)):
                    anio_ini = lista_fechas_inicio[i].year
                    mes_ini = str(lista_fechas_inicio[i].month).zfill(2)
                    dia_ini = str(lista_fechas_inicio[i].day).zfill(2)
                    anio_fin = lista_fechas_final[i].year
                    mes_fin = str(lista_fechas_final[i].month).zfill(2)
                    dia_fin = str(lista_fechas_final[i].day).zfill(2)
                    print(anio_ini)
                    print(mes_ini)
                    print(dia_ini)

                    address = "https://ws01.cenace.gob.mx:8082/SWPSC/SIM/"+sistema+"/"+proceso+"/"+str(anio_ini)+"/"+str(mes_ini)+"/"+str(dia_ini)+"/"+str(anio_fin)+"/"+str(mes_fin)+"/"+str(dia_fin)+"/json"
                    print(address)

                    info = requests.get(address).json()
                    proceso = info["proceso"]
                    sistema = info["sistema"]
                    info = info["Resultados"]

                    for i in range(len(info)):
                        temporal = pd.json_normalize(info[i], 'Valores')
                        temporal['clv_zona_reserva']="ZONA "+ str(i+1)
                        print(temporal.head(10))
                        temporal['proceso'] = proceso
                        temporal['sistema'] = sistema
                        appended_data_list.append(temporal)

                    appended_data = pd.concat(appended_data_list)
                    consultas_terminadas = consultas_terminadas + 1
                    status_text.set("Consultas terminadas: "+str(consultas_terminadas))

        csv_file = 'cenace_' + str(datetime.now().strftime('%Y_%m_%d_%H_%M_%S')) + '.csv'
        appended_data.to_csv(csv_file,index=False)
        status_text.set("Consulta exitosa!")

    except:
        status_text.set("Error en la consulta")




root = tk.Tk()

canvas = tk.Canvas(root, width = 500, height = 400,bg='white')
canvas.pack()

frame = tk.Frame(root,bg='#F2F2F2')
frame.place(relx=0.01,rely=0.025,relwidth=0.98,relheight=0.2)
texto_sistemas = tk.Label(frame,text = "SISTEMA", font='Arial 11 bold')
texto_sistemas.place(relx=0,rely=0,relwidth=1,relheight=0.5)
check_sin = tk.IntVar(value=1)
check_bca = tk.IntVar(value=1)
check_bcs = tk.IntVar(value=1)
C1 = tk.Checkbutton(frame,text="SIN",variable=check_sin)
C1.place(relx=0,rely=.5,relwidth=0.33,relheight=0.5)
C2 = tk.Checkbutton(frame,text="BCA",variable=check_bca)
C2.place(relx=0.33,rely=.5,relwidth=0.33,relheight=0.5)
C3 = tk.Checkbutton(frame,text="BCS",variable=check_bcs)
C3.place(relx=0.66,rely=.5,relwidth=0.33,relheight=0.5)

frame_2 = tk.Frame(root,bg='#F2F2F2')
frame_2.place(relx=0.01,rely=0.25,relwidth=0.98,relheight=0.2)
texto_procesos = tk.Label(frame_2,text = "PROCESO", font='Arial 11 bold')
texto_procesos.place(relx=0,rely=0,relwidth=1,relheight=0.5)
check_mda = tk.IntVar(value=1)
check_mtr = tk.IntVar(value=1)
C4 = tk.Checkbutton(frame_2,text="MDA",variable=check_mda)
C4.place(relx=0,rely=.5,relwidth=0.5,relheight=0.5)
C5 = tk.Checkbutton(frame_2,text="MTR",variable=check_mtr)
C5.place(relx=0.5,rely=.5,relwidth=0.5,relheight=0.5)

frame_3 = tk.Frame(root,bg='#F2F2F2')
frame_3.place(relx=0.01,rely=0.475,relwidth=0.98,relheight=0.2)
texto_procesos = tk.Label(frame_3,text = "PERIODO", font='Arial 11 bold')
texto_procesos.place(relx=0,rely=0,relwidth=1,relheight=0.5)
cal1 = DateEntry(frame_3,bg="darkblue",fg="white",year=2020,day=1,date_pattern="dd/mm/yy")
cal1.place(relx=0.1,rely=.5,relwidth=0.3,relheight=0.3)
cal2 = DateEntry(frame_3,bg="darkblue",fg="white",year=2020,date_pattern="dd/mm/yy")
cal2.place(relx=0.6,rely=.5,relwidth=0.3,relheight=0.3)

frame_4 = tk.Frame(root,bg='#F2F2F2')
frame_4.place(relx=0.01,rely=0.7,relwidth=0.98,relheight=0.1)
boton_calculo = tk.Button(frame_4,text="CONSULTAR", command=consulta)
boton_calculo.place(relx=0.375,rely=0.1,relwidth=0.25,relheight=0.8)

status_text = tk.StringVar()
status = tk.Label(root,textvariable=status_text,bg="white")
status.place(relx=0.00,rely=0.93,relwidth=0.5,relheight=0.05,anchor="w")
#status_text.set("Haz clic en CONSULTAR")

root.title("APP CENACE") 
root.mainloop()


#pyinstaller -F --hidden-import "babel.numbers" app_cenace.py