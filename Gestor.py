
from Colas import Cola, GeneralNoUrgente, GeneralUrgente, EspecificoNoUrgente, EspecificoUrgente, Admision
from clase_paciente import Paciente
import sys

class Gestor_Turnos:
    """
     Gestiona la distribución de los pacientes y el tiempo en el hospital.
 
    Gestiona la actualización de las unidades de tiempo en el hospital. Así como se encarga de cargar los pacientes desde el
    archivo .txt a la Cola de Admision, para distribuirlos en sus Colas correspondientes en función de su prioridad y tipo de
    consulta para después pasarlos a consulta y retirarlos cuando acaben su sesión.
 
    Methods :
    ---------
    actualizar_tiempo(self) : 
        Actualiza el tiempo del hospital en una unidad.

    cargar_pacientes(self) :
        Carga pacientes desde un archivo de texto y los almacena en la cola Admision.
    
    distribuir_pacientes(self, Admision) :
        Distribuye a los pacientes en sus colas correspondientes según el tipo de consulta y urgencia (True/False).
    
    pasar_consulta(self, consultas_colas: dict) :
        Pasa los pacientes a la consulta si estas están vacías.
    
    retirar_consulta(self, consultas_colas: dict) :
        Retira pacientes de la consulta y, si han esperado demasiado, los prioriza.
    """ 

    def __init__(self, tActual= 1) :
        """
        Inicializa el gestor de turnos con un tiempo actual y listas vacías.
        
        Attributes :
        -------------
        _tActual : = 1 (int)
            Tiempo actual del hospital.
        _lista_prioridad : list
            Lista de pacientes priorizados.
        _almacenamiento : list
            Almacén de pacientes tratados.
        """

        self._tActual = tActual
        self._lista_prioridad = []
        self._almacenamiento = []

    @property
    def almacenamiento(self) :
        """Devuelve la lista de pacientes almacenados."""
        
        return self._almacenamiento

    @property
    def tActual(self) :
        """Devuelve el tiempo actual del hospital."""
        
        return self._tActual

    @tActual.setter
    def tActual(self, value) :
        """Actualiza el tiempo actual, asegurando que sea un entero positivo."""

        if isinstance(value, int) and value >= 0:
            self._tActual = value
        else:
            raise ValueError("El tiempo actual tiene que ser un número entero positivo")
    
    @property
    def lista_prioridad(self) :
        """Devuelve la lista de pacientes prioritarios."""

        return self._lista_prioridad

                
#Consultas:
    G_Urgente = []
    G_NUrgente = []
    E_Urgente = []
    E_NUrgente = []
# Metodos
    def actualizar_tiempo(self) :
        """
        Actualiza el tiempo del hospital en una unidad.
        
        Return :
        --------
        None
        """

        self._tActual += 1
        return None

    
    def cargar_pacientes(self) :
        """
        Carga pacientes desde un archivo de texto y los almacena en la cola Admision.
        
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

    
    def distribuir_pacientes(self, Admision) :
        """
        Distribuye a los pacientes en sus colas correspondientes según el tipo de consulta y urgencia (True/False).
        
        Return :
            None
        """

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
        return None


    def pasar_consulta(self, consultas_colas: dict) :
        """
        Pasa los pacientes a la consulta si estas están vacías.
        
        Return :
        --------
            None
        """

        for lista in consultas_colas.keys():
            if not lista.is_empty() and len(consultas_colas[lista]) == 0:
                paciente = lista.dequeue()
                paciente.tiempos["tInicio_consulta"] = self.tActual
                consultas_colas[lista].append(paciente)
                print(f"{self.tActual}: {paciente.IDPac} entra {paciente.consulta}/Urgente: {paciente.urgencia} ADM:{paciente.tiempos['tEntrada']}, INI: {paciente.tiempos['tInicio_consulta']}, EST: {paciente.tEstimado}")
        return None
    

    def retirar_consulta(self, consultas_colas: dict) :
        """
        Retira pacientes de la consulta y, si han esperado demasiado, los prioriza.
        
        Return :
        --------
            None
        """

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
                        consultas.remove(paciente)
        return None