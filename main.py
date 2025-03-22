# Clases / Librerías

import sys
from Gestor import Gestor_Turnos
from clase_paciente import Paciente
from Colas import Cola
# Funciones

def cargar_paciente(cola: Cola) : 
        # Leer el archivo de configuración desde la línea de comandos o usar el predeterminado
        config_file = sys.argv[1] if len(sys.argv) > 1 else "./patients0.txt"
    
        # Intentar abrir el archivo especificado
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"Error: El archivo '{config_file}' no existe.", file = sys.stderr)
            sys.exit(1)
    
        for i in range(len(lines)):
            datos_paciente = lines[i].split()
            IDPac = datos_paciente[0]
            consulta = datos_paciente[1]
            urgencia = datos_paciente[2].lower() == "true"
            tEstimado = int(datos_paciente[3])
            
            paciente = Paciente(IDPac, consulta, urgencia)
            paciente.tiempos['tEstimado'] = tEstimado
            cola.enqueue(paciente)            
            return

# Código main()

if __name__ == '__main__' :
    admision = Gestor_Turnos.Admision
    cargar_paciente(admision)
    print(admision)
    