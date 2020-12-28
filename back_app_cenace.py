import requests
import pandas as pd
from datetime import datetime
from datetime import date

lista_sistemas = ["SIN","BCA","BCS"]
lista_sistemas = ["SIN"]
sistema = "SIN"
lista_procesos = ["MDA","MTR"]
proceso = "MDA"
anio_ini = "2020"
mes_ini = "12"
dia_ini = "1"
anio_fin = "2020"
mes_fin = "12"
dia_fin = "1"

fecha_ini = date(int(anio_ini), int(mes_ini), int(dia_ini))
fecha_fin = date(int(anio_fin), int(mes_fin), int(dia_fin))
delta = fecha_fin - fecha_ini
delta = delta.days

mod_fecha = delta % 7 
div_fecha = delta // 7 

lista_fechas_inicio=[]
lista_fechas_final=[]
lista_fechas_inicio.append(fecha_ini)
for i in range(div_fecha):    
    lista_fechas_final.append(lista_fechas_inicio[-1]+datetime.timedelta(days=6))
    lista_fechas_inicio.append(lista_fechas_inicio[-1]+datetime.timedelta(days=7))
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
csv_file = 'cenace_' + str(datetime.now().strftime('%Y_%m_%d_%H_%M_%S')) + '.csv'
appended_data.to_csv(csv_file,index=False)
