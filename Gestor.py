
from Colas import Cola, GeneralNoUrgente, GeneralUrgente, EspecificoNoUrgente, EspecificoUrgente, Admision
from clase_paciente import Paciente
import sys

class Gestor_Turnos:
    def __init__(self, tActual= 0):
        self._tActual = tActual
        self._lista_prioridad = []

    @property
    def tActual(self):
        return self._tActual

    @tActual.setter
    def tActual(self, value):
        if isinstance(value, int) and value >= 0:
            self._tActual = value
        else:
            raise ValueError("El tiempo actual tiene que ser un número entero positivo")

                
                
#Consultas:
    G_Urgente = []
    G_NUrgente = []
    E_Urgente = []
    E_NUrgente = []
# Metodos
    def actualizar_tiempo(self):
        self._tActual += 1

    
#Carga los pacientes del txto todos a la vez
    def cargar_pacientes(self):
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

        
    #Cada paciente lo incluyes en en su cola correspondiente
    def distribuir_pacientes(self):
        if self.tActual % 3 == 0 and not Admision.is_empty():
            paciente = Admision.dequeue()
            paciente.tiempos["tEntrada"] = self.tActual
            if paciente.consulta == "general":
               if paciente.urgencia:
                   GeneralUrgente.enqueue(paciente)
                   print(f"{paciente.IDPac} entro en la cola General Urgente")                   
               else:
                   GeneralNoUrgente.enqueue(paciente)
                   print(f"{paciente.IDPac} entro en la cola General No Urgente")
                   
            elif paciente.consulta == "specialist":
               if paciente.urgencia:
                   EspecificoUrgente.enqueue(paciente)
                   print(f"{paciente.IDPac} entro en la cola Especifico Urgente")
               else:
                   EspecificoNoUrgente.enqueue(paciente)
                   print(f"{paciente.IDPac} entro en la cola Especifico No Urgente")

        return None
            
            

    #Molaria poder meterle el nombre de la consulta a la que va
    def pasar_consulta(self, consultas_colas: dict):
        for lista in consultas_colas.keys():
            if not lista.is_empty() and len(consultas_colas[lista]) == 0:
                en_consulta = lista.dequeue()
                en_consulta.tiempos["tInicioConsulta"] = self.tActual
                consultas_colas[lista].append(en_consulta)
                print(f"{en_consulta.IDPac} ha pasado a consulta; tiempo estimado: {en_consulta.tEstimado} horas")
        return None
                
     


          
#Sirve para enlazar cada cola a su correspondiente consulta:        
consultas_colas = {GeneralNoUrgente: Gestor_Turnos.G_NUrgente, GeneralUrgente: Gestor_Turnos.G_Urgente, EspecificoNoUrgente: Gestor_Turnos.E_NUrgente, EspecificoUrgente: Gestor_Turnos.E_Urgente}



a = Gestor_Turnos()
a.cargar_pacientes()
for i in range(6):
    a.distribuir_pacientes()
    
a.pasar_consulta(consultas_colas)


print(GeneralNoUrgente.first().tiempos) 

 ######TO DO:
     #Incluir el contador en descenso por cada vez que turno que pasa y verificar si tFinalConsulta - tInicioConsulta >= tEstimado
     #Metodo para vaciar las consultas una vez haya terminado de tratarse cada paciente
     #Funcion de prioridad, control del tiempo que lleva cada paciente en cola (podriamos añadir un nuevo tiempo tEspera que si >= 7 entonces le da prio)
     #Asignar los valores de tiempo a cada paciente 
     #Asignar los tiempos en paciente.tiempos
     #Volver a poner lo de cargar pacientes en el main (sorry)
     #Matarse. :D
     
