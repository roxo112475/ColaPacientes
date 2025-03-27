# Clases / Librerías

import sys
from Gestor import Gestor_Turnos
from clase_paciente import Paciente
from Colas import Cola, GeneralNoUrgente, GeneralUrgente, EspecificoNoUrgente, EspecificoUrgente, Admision
# Funciones

def cargar_pacientes(self: Gestor_Turnos):
    # Leer el archivo de configuración desde la línea de comandos o usar el predeterminado
    config_file = sys.argv[1] if len(sys.argv) > 1 else "./patients0.txt"

    # Intentar abrir el archivo especificado
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: El archivo '{config_file}' no existe.", file=sys.stderr)
        sys.exit(1)
    Admision.clear() #Así solo guarda en admision los pacientes dek txt y no se acumulan entre ejecuciones
    
    for i in range(len(lines)):
        datos_paciente = lines[i].split()
        IDPac = datos_paciente[0]
        consulta = datos_paciente[1]
        urgencia = datos_paciente[2].lower() == "true"
        tEstimado = int(datos_paciente[3])
        paciente = Paciente(IDPac, consulta, urgencia, tEstimado)
        paciente.tiempos["tLlegada"] = self.tActual
        Admision.enqueue(paciente)            

    return None

# Código main()

if __name__ == '__main__' :
    
    # Creacion de la cola de admision
    gestor = Gestor_Turnos()
    Admision.enqueue(cargar_pacientes(gestor))
    lista_prioridad = []
    
    consultas_dict = {GeneralNoUrgente: [], GeneralUrgente: [], EspecificoNoUrgente: [], EspecificoUrgente: []}

    Ejecutar = True

    while Ejecutar:
        gestor.distribuir_pacientes(Admision, GeneralNoUrgente, GeneralUrgente, EspecificoNoUrgente, EspecificoUrgente, lista_prioridad)
        # falta arreglar #
        gestor.retirar_consulta(Admision, GeneralNoUrgente, GeneralUrgente, EspecificoNoUrgente, EspecificoUrgente, lista_prioridad) 
        # falta arreglar #
        gestor.pasar_consulta(consultas_dict)
        
        gestor.actualizar_tiempo()
        print()
        
        
        # Comprobacion fiin de ejecucion
        if Admision.is_empty() and all(colas.is_empty() for colas in consultas_colas.keys()) and all(len(consultas) == 0 for consultas in consultas_colas.values()):
            Ejecutar = False

        
    """
Ejecutar = True
Gestor = Gestor_Turnos()
Gestor.cargar_pacientes()
while Ejecutar:
    Gestor.distribuir_pacientes()   
    Gestor.retirar_consulta(consultas_colas)     
    Gestor.pasar_consulta(consultas_colas)
      
    Gestor.actualizar_tiempo()
    print()
    
    if Admision.is_empty() and all(colas.is_empty() for colas in consultas_colas.keys()) and all(len(consultas) == 0 for consultas in consultas_colas.values()):
        Ejecutar = False
""" 