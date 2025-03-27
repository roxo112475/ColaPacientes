# Clases / Librerías

import sys
from Gestor import Gestor_Turnos
from clase_paciente import Paciente
from Colas import Cola, GeneralNoUrgente, GeneralUrgente, EspecificoNoUrgente, EspecificoUrgente, Admision
import pandas 

def estadisticas(Gestor):
    priorizaciones_aplicadas = Gestor.numero_prios

    datos = pandas.DataFrame(Gestor.almacenamiento, columns = ["IDPac","Consulta", "Urgencia", "tEstimado", "Tiempos" ])
    datos["Priorizaciones"] = priorizaciones_aplicadas

    datos_general = datos.loc[datos["Consulta"] == "general"] #DataFrames filtrados para consultas Generales
    datos_especialidad = datos.loc[datos["Consulta"] == "specialist"] #DataFrames filtrados para consultas Especialidad



    media_priorizaciones = datos.groupby("Consulta")["Priorizaciones"].mean().fillna(0) #ESTO DA MAL, NO SE PUEDE METER EL DATO ASI EN EL DFRAMWE
    print(media_priorizaciones)

    tiempo_medio_espera = datos.groupby(["Consulta", "Urgencia"]).mean()
    print(tiempo_medio_espera)
















# Código main()

consultas_colas = {GeneralNoUrgente: Gestor_Turnos.G_NUrgente, GeneralUrgente: Gestor_Turnos.G_Urgente, EspecificoNoUrgente: Gestor_Turnos.E_NUrgente, EspecificoUrgente: Gestor_Turnos.E_Urgente}

if __name__ == '__main__' :
    Gestor = Gestor_Turnos()    
    
    Ejecutar = True

    Gestor.cargar_pacientes()
    while Ejecutar:
        Gestor.distribuir_pacientes(Admision)   
        Gestor.retirar_consulta(consultas_colas)     
        Gestor.pasar_consulta(consultas_colas)
          
        Gestor.actualizar_tiempo()

        
        if Admision.is_empty() and all(colas.is_empty() for colas in consultas_colas.keys()) and all(len(consultas) == 0 for consultas in consultas_colas.values()):
            Ejecutar = False
    print()
    estadisticas(Gestor)