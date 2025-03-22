
class Paciente:
    def __init__(self, IDPac: int, consulta: str, urgencia: bool, tEstimado: int):
        self.IDPac = IDPac
        self.consulta = consulta
        self.urgencia = urgencia
        self.tEstimado = tEstimado
        self.tiempos = {"tEstimado": tEstimado, "tLlegada": None, "tEntrada": None, "tInicio_consulta": None, "tFinal_consulta": None, "tTotal": None }
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
    def tEstimado(self):
        return self._tEstimado
    
    
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
                  
              
    @tEstimado.setter
    def tEstimado(self, value):
        if isinstance(value, int) and value > 0:
            self._tEstimado = value 
        else:
            raise ValueError("El tiempo estimado tiene que tener un entero positivo")
        
    def __str__(self):
        return f"ID: {self.IDPac}, Tipo de Consulta: {self.consulta}, Urgencia: {self.urgencia}, Tiempo Estimado: {self.tEstimado}"
    