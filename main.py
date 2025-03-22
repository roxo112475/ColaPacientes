# Clases / Librerías

import sys
import Gestor
import clase_paciente as paciente
import Cola from Colas
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
            if not any( admitidos.IDPac() == IDPac for admitidos in cola.Admision()):
                paciente = Paciente(IDPac, consulta, urgencia, tEstimado)
                cola.Admision().enqueue(paciente)            
                return

# Código main()

if __main__ == '__name__' :
    Gestor.Admision() = cargar_paciente()
    print(Gestor.Admision())
    