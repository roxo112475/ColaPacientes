
class Paciente:
    def __init__(self, IDPac: int, consulta: str, urgencia: bool, tEstimado: int):
        self.IDPac = IDPac
        self.consulta = consulta
        self.urgencia = urgencia
        self.tEstimado = tEstimado

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
        if isinstance(value, int) and value > 0:
            self._IDPac = value
        else:
            raise TypeError("El ID del Paciente tiene que ser un numero mayor que 0")

    @consulta.setter
    def consulta(self, value):
        if isinstance(value, str) and value in ["General", "Especialidad"]:
            self._consulta = value.capitalize
        else:
            raise TypeError("No es un tipo de consulta valido")

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
            raise TypeError("El tiempo estimado tiene que tener un entero positivo")
        
    
paciente_1 = Paciente(1, "General", False, 15)