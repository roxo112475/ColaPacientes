
from Colas import Cola
from clase_paciente import Paciente
import sys

class Gestor_Turnos:
    def __init__(self):
        self._GeneralUrgente = Cola()
        self._GeneralNoUrgente = Cola()
        self._EspecificoUrgente = Cola()
        self._EspecificoNoUrgente = Cola()
        self._Admision = Cola()
        
        
#Properties y setters

    @property
    def GeneralUrgente(self) :
        return self._GeneralUrgente
    
    @GeneralUrgente.setter
    def GeneralUrgente(self, value) :
        if isinstance(value, Cola):
            if all(pacientes.consulta == 'general' for pacientes in value) and all(pacientes.urgencia for pacientes in value ):
                self._GeneralUrgente = value    
            else:
                raise TypeError('Hay pacientes que no pertenecen a la cola de atención general urgente.')
        else:        
            raise TypeError("El valor debe ser una instancia de Cola.")
    
 
    
    @property
    def GeneralNoUrgente(self) :
        return self._GeneralNoUrgente
    
    @GeneralNoUrgente.setter
    def GeneralNoUrgente(self, value):
        if isinstance(value, Cola):
            if all(pacientes.consulta == 'general' for pacientes in value) and all(not pacientes.urgencia for pacientes in value ):
                self._GeneralNoUrgente = value
         
            else:
                raise TypeError('Hay pacientes que no pertenecen a la cola de atención general no urgente.')
        else:
            raise TypeError("El valor debe ser una instancia de Cola.")
               
            
            
    @property
    def EspecificoUrgente(self):
        return self._EspecificoUrgente
    
    @EspecificoUrgente.setter
    def EspecificoUrgente(self, value):
        if isinstance(value, Cola):
            if all(pacientes.consulta == "specialist" for pacientes in value) and all(pacientes.urgencia for pacientes in value): 
                self._EspecificoUrgente = value
            else:
                raise TypeError("Hay pacientes que no pertenecen a la cola de atención especifica urgente")
        else:
            raise TypeError("El valor debe ser una instancia de Cola.")
    

    
    @property
    def EspecificoNoUrgente(self):
        return self._EspecificoNoUrgente
    
    @EspecificoNoUrgente.setter
    def EspecificoNoUrgente(self, value):
        if isinstance(value, Cola):
            if all(pacientes.consulta == "specialist" for pacientes in value) and all(not pacientes.urgencia for pacientes in value):
                self._EspecificoNoUrgente = value
            else:
                raise TypeError("Hay pacientes que no pertenecen a la cola de atención especifica no urgente")
        else:
            raise TypeError("El valor debe ser una instancia de Cola.")
            
           
    
    @property
    def Admision(self):
        return self._Admision
    
    @Admision.setter
    def Admision(self,value):
        if isinstance(value, Cola):
            self._Admision = value
        else:
            raise TypeError("El valor debe ser una instancia de cola")
            
            
            
            
# Metodos

    #A esto le falta cargar solamente 1 por vez que se llama a la funcion
    def cargar_paciente(self): 
        # Leer el archivo de configuración desde la línea de comandos o usar el predeterminado
        config_file = sys.argv[1] if len(sys.argv) > 1 else "./patients0.txt"
    
        # Intentar abrir el archivo especificado
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"Error: El archivo '{config_file}' no existe.", file=sys.stderr)
            sys.exit(1)
    
        for i in range(len(lines)):
            datos_paciente = lines[i].split()
            IDPac = datos_paciente[0]
            consulta = datos_paciente[1]
            urgencia = datos_paciente[2].lower() == "true"
            tEstimado = int(datos_paciente[3])
            if not any( admitidos.IDPac == IDPac for admitidos in self.Admision):
                paciente = Paciente(IDPac, consulta, urgencia, tEstimado)
                self.Admision.enqueue(paciente)            
                return
        




a = Gestor_Turnos()

a.cargar_paciente()

print(a.Admision)













