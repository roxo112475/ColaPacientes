# Clases / Librerías

import sys
from Gestor import Gestor_Turnos
from clase_paciente import Paciente
from Colas import Cola, GeneralNoUrgente, GeneralUrgente, EspecificoNoUrgente, EspecificoUrgente, Admision
import pandas as pd


# functions

def media_ColaEspera(registro: dict) :
    """
    Para el registro de tiempos por consulta, hace su media y lo almacena.

    Return :
    --------
        dict : diccionario con las medias de los 'values' originales.
    """
    aux = 0

    for consulta in registro :
        
        for paciente in range(len(registro[consulta])) :
            if not isinstance(registro[consulta][paciente], int) or registro[consulta][paciente] < 0 :
                raise ValueError('Los datos de tiempo de espera en cola deben ser enteros positivos.')

            aux += registro[consulta][paciente]
        registro[consulta] = aux
        aux = 0

    return registro


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
    
    registro = media_ColaEspera(Gestor.tiempoCola)
    registro = pd.DataFrame(registro)
    print(registro)
