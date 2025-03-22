
class Paciente:
    def __init__(self, IDPac: int, consulta: str, urgencia: bool, tEstimado: int):
        self.IDPac = IDPac
        self.consulta = consulta
        self.urgencia = urgencia
        self.tiempos = {"tEstimado": None, "tLlegada": None, "tEntrada": None, "tInicio_consulta": None, "tFinal_consulta": None, "tTotal": None }
#Propiedades: 

    @property
    def IDPac(self):
        return self._IDPac
    
    @property
    def consulta(self):
        return self._consulta 
    
    @property
    def urgencia(self):
        return self._urgencia
    @property
    def tiempos(self):
        return self._tiempos
    
    
    #Setters
    @IDPac.setter
    def IDPac(self, value):
        if isinstance(value, str) and len(value) !=  0:
            self._IDPac = value
        else:
            raise TypeError("El ID del Paciente tiene que ser una cadena no vacia")

    @consulta.setter
    def consulta(self, value):
        if isinstance(value, str) and value.lower() in ["general", "specialist"]:
            self._consulta = value.lower()
        else:
            raise ValueError("Tipo de consulta no válido. Debe ser 'general' o 'specialist'.")
            

    @urgencia.setter
    def urgencia(self, value):
        if isinstance(value, bool):
            self._urgencia = value

        else:
            raise TypeError("La variable tiene que ser de tipo booleano ")
                  
              
    @tiempos.setter
    def tiempos(self, value):
        for i in self._tiempos :
            if isinstance(value[i], int) and value[i] > 0:
                self._tiempos = value[i] 
            else :
                raise ValueError("El tiempo estimado tiene que tener un entero positivo")
        
        if value['tFinalConsulta'] < value['tInicioConsulta'] < value['tLlegada'] :
            raise ValueError('La cronología de accesos no es lineal.')
        
        if value['tFinalConsulta'] - value['tInicioConsulta'] > value['tEstimado'] :
            raise ValueError('El tiempo de consulta ha superado al estimado.')
        
        if value['tTotal'] != value['tFinalConsulta'] - value['tLlegada'] :
            raise ValueError('El tiempo total no representa el tiempo real del paciente en espera y consulta.')
        
        if value['tEntrada'] < value['tLlegada'] :
            raise ValueError('El tiempo de entrada a la cola no puede ser menor al de llegada a admisión.')
        
    def __str__(self):
        return f"ID: {self.IDPac}, Tipo de Consulta: {self.consulta}, Urgencia: {self.urgencia}, Tiempo Estimado: {self.tEstimado}"
    