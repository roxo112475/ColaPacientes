# García Iglesias, Nicolás - nicolas.garcia.iglesias@udc.es
# Omil Barreiro, Manuel - manuel.omil.barreiro@udc.es

import sys
import pandas as pd
from gestor import Gestor_Turnos
from clase_paciente import Paciente
from colas import (
    GeneralNoUrgente, GeneralUrgente,
    EspecificoNoUrgente, EspecificoUrgente, Admision
)

#Carga del archivo a los pacientes, los genera y los pasa a la cola de admision
def cargar_pacientes(Admision):
    """
    Lee un archivo .txt del que extrae los datos de los pacientes.

    Return : 
    --------
        None
    """
    # Leer el archivo de configuración desde la línea de comandos o usar el predeterminado
    config_file = sys.argv[1] if len(sys.argv) > 1 else "./patients0.txt"

    # Intentar abrir el archivo especificado
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: El archivo '{config_file}' no existe.", file=sys.stderr)
        sys.exit(1)
    Admision.clear() #Así solo guarda en admision los pacientes del .txt y no se acumulan entre ejecuciones
    
    for i in range(len(lines)):
        datos_paciente = lines[i].split()
        IDPac = datos_paciente[0]
        consulta = datos_paciente[1]
        urgencia = datos_paciente[2].lower() == "true"
        tEstimado = int(datos_paciente[3])
        paciente = Paciente(IDPac, consulta, urgencia, tEstimado)
        Admision.enqueue(paciente)            

    return None



def estadisticas(registro: dict, media_prios: dict):
    """
    Calcula estadísticas sobre el tiempo de espera y priorización de pacientes.
    
    Parámetros:
    -----------
    registro : dict
        Diccionario con listas de tiempos de espera para cada tipo de consulta.
    media_prios : dict
        Diccionario con el conteo de priorizaciones por tipo de consulta.
    
    Excepciones:
    ------------
    ValueError
        Si los datos de tiempo de espera en cola no son enteros positivos.
    
    Retorno:
    --------
    None
    """
    #Media de priorizaciones aplicadas por tipo de consulta

    total_general = sum(1 for pacientes in Gestor.almacenamiento if pacientes.consulta == "general") #Numero de pacientes de cada tipo
    total_especifico = len(Gestor.almacenamiento) - total_general
    
    if total_general:
        media_prios["general"] /= total_general
    if total_especifico:
        media_prios["especialidad"] /= total_especifico
    
    media_prios_df = pd.DataFrame.from_dict(media_prios, orient='index', columns=['Nº Medio de Citas con Priorización'])
    
    #Media de tiempo de espera por tipo de cola:

    for consulta, tiempos in registro.items():
        if any(not isinstance(tiempo, int) or tiempo < 0 for tiempo in tiempos):
            raise ValueError('Los datos de tiempo de espera deben ser enteros positivos.')
        if len(tiempos) != 0 : #Evitar division entre 0
            registro[consulta] = sum(tiempos) / len(tiempos) 
        else:
            registro[consulta] = 0
    
    registro_df = pd.DataFrame.from_dict(registro, orient='index', columns=['Tiempo Medio en Cola'])

    #Print de resultados
    print(media_prios_df.to_string(justify='center'))
    print("\n", registro_df.to_string(justify='center'), "\n")
    


#Ejecucion
if __name__ == '__main__':
    Gestor = Gestor_Turnos()


    #Diccionario que relaciona las colas a las consultas
    consultas_colas = {
        GeneralNoUrgente: Gestor.G_NUrgente,
        GeneralUrgente: Gestor.G_Urgente,
        EspecificoNoUrgente: Gestor.E_NUrgente,
        EspecificoUrgente: Gestor.E_Urgente
    }
    

    cargar_pacientes(Admision)
    #Bucle de ejecucion
    while not (Admision.is_empty() and all(colas.is_empty() for colas in consultas_colas.keys()) 
               and all(not consultas for consultas in consultas_colas.values())): #Comprueba que colas, consultas y la lista de admision estan vacias antes de parar
        Gestor.distribuir_pacientes(Admision)
        Gestor.retirar_consulta(consultas_colas)
        Gestor.pasar_consulta(consultas_colas)
        Gestor.actualizar_tiempo()
    
    #Print de las estadisticas del panda
    estadisticas(Gestor.tiempoCola, Gestor.numero_prios)
