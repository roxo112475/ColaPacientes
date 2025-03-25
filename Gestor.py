
from Colas import Cola, GeneralNoUrgente, GeneralUrgente, EspecificoNoUrgente, EspecificoUrgente, Admision
from clase_paciente import Paciente
import sys

class Gestor_Turnos:
    def __init__(self, tActual= 1):
        self._tActual = tActual
        self._lista_prioridad = []
        self._almacenamiento = []

    @property
    def almacenamiento(self):
        return self._almacenamiento

    @property
    def tActual(self):
        return self._tActual

    @tActual.setter
    def tActual(self, value):
        if isinstance(value, int) and value >= 0:
            self._tActual = value
        else:
            raise ValueError("El tiempo actual tiene que ser un número entero positivo")
    
    @property
    def lista_prioridad(self):
        return self._lista_prioridad

                
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
    def distribuir_pacientes(self, Admision):
        if self.tActual %  3 == 1 and not Admision.is_empty():

            paciente = Admision.dequeue()
            paciente.tiempos["tEntrada"] = self.tActual
            
            if paciente.consulta == "general":
               if paciente.urgencia or paciente.IDPac in self.lista_prioridad:
                   if paciente.IDPac in self.lista_prioridad:
                       print(f"{self.tActual}: Priorización aplicada {paciente.IDPac}")
                       self.lista_prioridad.remove(paciente.IDPac)
                       
                   GeneralUrgente.enqueue(paciente)
                   print(f"{self.tActual}: {paciente.IDPac} en cola {paciente.consulta}/Urgente: {paciente.urgencia} EST:{paciente.tEstimado}")    
                   
               else:
                   GeneralNoUrgente.enqueue(paciente)
                   print(f"{self.tActual}: {paciente.IDPac} en cola {paciente.consulta}/Urgente: {paciente.urgencia} EST:{paciente.tEstimado}")
                   
                   
            elif paciente.consulta == "specialist":
               if paciente.urgencia or paciente.IDPac in self.lista_prioridad:
                   if paciente.IDPac in self.lista_prioridad:
                       print(f"{self.tActual}: Priorización aplicada {paciente.IDPac}")
                       self.lista_prioridad.remove(paciente.IDPac)
                       
                   EspecificoUrgente.enqueue(paciente)
                   print(f"{self.tActual}: {paciente.IDPac} en cola {paciente.consulta}/Urgente: {paciente.urgencia} EST:{paciente.tEstimado}")
                   
               else:
                   EspecificoNoUrgente.enqueue(paciente)
                   print(f"{self.tActual}: {paciente.IDPac} en cola {paciente.consulta}/Urgente: {paciente.urgencia} EST:{paciente.tEstimado}")


            
            

    #Molaria poder meterle el nombre de la consulta a la que va
    #Pasa a los pacientes de las colas a las consultas donde se les tratan (si estan libres)
    def pasar_consulta(self, consultas_colas: dict):
        for lista in consultas_colas.keys():
            if not lista.is_empty() and len(consultas_colas[lista]) == 0:
                paciente = lista.dequeue()
                paciente.tiempos["tInicio_consulta"] = self.tActual
                consultas_colas[lista].append(paciente)
                print(f"{self.tActual}: {paciente.IDPac} entra {paciente.consulta}/Urgente: {paciente.urgencia} ADM:{paciente.tiempos['tEntrada']}, INI: {paciente.tiempos['tInicio_consulta']}, EST: {paciente.tEstimado}")

    
    
    #Retira de la consulta a los pacientes ya tratados y se les aplica el tTotal y la priorizacion
    def retirar_consulta(self, consultas_colas: dict) :
        for consultas in consultas_colas.values() :
            if len(consultas) != 0 :
                paciente = consultas[0]

                if (self.tActual - paciente.tiempos["tInicio_consulta"]) >= paciente.tEstimado:
                    paciente.tiempos["tFinal_consulta"] = self.tActual
                    paciente.tiempos["tTotal"] = (self.tActual - paciente.tiempos["tEntrada"])
                    self.almacenamiento.append(paciente)
                    
                    if paciente.tiempos["tInicio_consulta"] - paciente.tiempos["tEntrada"] >= 7 :
                        a = consultas.pop(0)
                        print(f'{self.tActual}: {paciente.IDPac} sale {paciente.consulta}/Urgente: {paciente.urgencia} ADM:{paciente.tiempos['tEntrada']}, INI: {paciente.tiempos['tInicio_consulta']}, EST./TOTAL: {paciente.tiempos['tEstimado']}/{paciente.tiempos['tTotal']}')
                        print(f"{self.tActual}: Priorización activa {paciente.IDPac}")
                        self.lista_prioridad.append(a.IDPac)
                        
                    else:
                        print(f"{self.tActual}: {paciente.IDPac} sale {paciente.consulta}/Urgente: {paciente.urgencia} ADM:{paciente.tiempos['tEntrada']}, INI: {paciente.tiempos['tInicio_consulta']}, EST./TOTAL: {paciente.tiempos['tEstimado']}/{paciente.tiempos['tTotal']}")
                        consultas.remove(paciente) #Si no se cumplen los requisitos no devuelve nada y lo quita de consulta
                       


"""
#La funcion retirar consulta probablemente se tenga que hacer asi
pacientes_tratados = retirar(consulta)
for pacientes in pacientes tratados:
    self.lista_prioridad.append(pacientes.IDPac) 
"""
          
#Sirve para enlazar cada cola a su correspondiente consulta:        
consultas_colas = {GeneralNoUrgente: Gestor_Turnos.G_NUrgente, GeneralUrgente: Gestor_Turnos.G_Urgente, EspecificoNoUrgente: Gestor_Turnos.E_NUrgente, EspecificoUrgente: Gestor_Turnos.E_Urgente}





    






#La clase de admision tiene que estar vacia y las colas tambien (implementar)

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
 ######TO DO:
     #Incluir el contador en descenso por cada vez que turno que pasa y verificar si tFinalConsulta - tInicioConsulta >= tEstimado
     #Metodo para vaciar las consultas una vez haya terminado de tratarse cada paciente (Lo mismo)
     #Funcion de prioridad, control del tiempo que lleva cada paciente en cola (podriamos añadir un nuevo tiempo tEspera que si >= 7 entonces le da prio)  (función retirar_Consulta)
     #Asignar los valores de tiempo a cada paciente (Hechos)
     #Asignar los tiempos en paciente.tiempos  (Hechos la mayoria)
     #Volver a poner lo de cargar pacientes en el main (sorry)
     #Matarse. :D
     
###HAY QUE ELIMINAR A LOS PACIENTES YA TRATADOS CON PRIORIZACION ACTIVA DE LA LISTA
##PARA LAS ESTADISTICAS TENDREMOS QUE GUARDAR LOS DATOS DE LOS PACIENTES (SOLO HACE FALTA LOS DICCIONARIOS SUPONGO)

###El problema tiene que estar en cargar_pacientes() porque carga todo el rato la misma lista y la vacia cada vez que se le llama


#Almacenamiento en el innit hacer los appends directamente,llamar a self.lista_prioridad para guardar ahi los IDs




