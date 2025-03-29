# Clases / Librerías

import sys
from Gestor import Gestor_Turnos
from clase_paciente import Paciente
from Colas import Cola, GeneralNoUrgente, GeneralUrgente, EspecificoNoUrgente, EspecificoUrgente, Admision
import pandas as pd


# functions

def estadisticas(registro: dict, media_prios: dict ) :

    """
    Para el registro de tiempos por consulta, hace su media y lo almacena.

    Exception :
    -----------
        ValueError : Cuando los datos de tiempo de espera en cola no son enteros positivos.

    Return :
    --------
        dict : diccionario con las medias de los 'values' originales.
    """
    aux = 0

    #Numero total de pacientes de cada tipo 
    total_general = 0
    total_especifico = 0

    #Media Priorizaciones:
    for paciente in Gestor.almacenamiento:
        if paciente.consulta == "general":
            total_general += 1
        else:
            total_especifico += 1


    media_prios["general"] = media_prios["general"]/total_general
    media_prios["especialidad"] = media_prios["especialidad"]/ total_especifico


    media_prios = pd.DataFrame.from_dict(media_prios, orient='index', columns=['Numero Medio De Citas Con Priorizacion Aplicada' ])
  


    #Tiempo Medio de Espera
   
    for consulta in registro :
        
        for paciente in range(len(registro[consulta])) :
            if not isinstance(registro[consulta][paciente], int) or registro[consulta][paciente] < 0 :
                raise ValueError('Los datos de tiempo de espera en cola deben ser enteros positivos.')

            aux += registro[consulta][paciente]
        registro[consulta] = aux/len(registro[consulta])
        aux = 0

    
    registro = pd.DataFrame.from_dict(registro, orient='index', columns=['Tiempo Medio De Permanencia En Las Colas'])

    print(registro, "\n")
    print(media_prios)




# Código main()

if __name__ == '__main__' :
    Gestor = Gestor_Turnos()    
    consultas_colas = {GeneralNoUrgente: Gestor_Turnos.G_NUrgente, GeneralUrgente: Gestor_Turnos.G_Urgente, EspecificoNoUrgente: Gestor_Turnos.E_NUrgente, EspecificoUrgente: Gestor_Turnos.E_Urgente}
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
    
    estadisticas(Gestor.tiempoCola, Gestor.numero_prios)