# García Iglesias, Nicolás - nicolas.garcia.iglesias@udc.es
# Omil Barreiro, Manuel - manuel.omil.barreiro@udc.es

class Paciente:
    """
    Inicializa a cada paciente.

    Crea su ID, indica su tipo de consulta, la urgencia de su caso y el tiempo estimado que le tomará
    en consulta.
    """

    def __init__(self, IDPac: int, consulta: str, urgencia: bool, tEstimado: int) :
        """
        Inicializa un paciente con sus propios atributos.
        
        Attributes :
        -------------
        _IDPac : int
            Identificador de paciente (distinto para cada paciente).
        _consulta : str
            Tipo de consulta (General / Específica).
        _urgencia : bool
            True para alta prioridad, False para prioiridad baja.
        """

        self.IDPac = IDPac
        self.consulta = consulta
        self.urgencia = urgencia
        self.tEstimado = tEstimado
        self.tiempos = {"tEstimado": tEstimado,  "tEntrada": -1, "tInicio_consulta": -1, "tFinal_consulta": -1, "tTotal": -1 }


#Propiedades: 
    @property
    def IDPac(self) :
        """Devuelve el identificador del paciente"""

        return self._IDPac


    @property
    def consulta(self):
        """Devuelve el tipo de consulta del paciente."""
        
        return self._consulta 
    
    @property
    def urgencia(self):
        """Devuelve True en caso de ser urgente y False sino.   """
        
        return self._urgencia


    @property
    def tEstimado(self):
        """Devuelve el tiempo estimado del paciente dentro de consulta."""
        
        return self._tEstimado
    
    
    #Setters
    @IDPac.setter
    def IDPac(self, value):
        """Establece el identificador del paciente, cuidando que no sea un string y que no sea una cadena vacía"""

        if isinstance(value, str) and len(value) !=  0:
            self._IDPac = value
        else:
            raise TypeError("El ID del Paciente tiene que ser una cadena no vacia")

    @consulta.setter
    def consulta(self, value):
        """Establece el tipo de consulta cuidando que sea el string 'general' o 'especialist' ."""

        if isinstance(value, str) and value.lower() in ["general", "specialist"]:
            self._consulta = value.lower()
        else:
            raise ValueError("Tipo de consulta no válido. Debe ser 'general' o 'specialist'.")
            

    @urgencia.setter
    def urgencia(self, value):
        """Estabece la urgencia en función de un booleano. True para prioritario y False para no prioritario."""

        if isinstance(value, bool):
            self._urgencia = value

        else:
            raise TypeError("La variable tiene que ser de tipo booleano ")
                  
              
    @tEstimado.setter
    def tEstimado(self, value):
        """Establece el tiempo estimado de consulta para el paciente. Cuida que sea un entero positivo"""

        if isinstance(value, int) and value > 0:
            self._tEstimado = value 
        else:
            raise ValueError("El tiempo estimado tiene que tener un entero positivo")
        
    def __str__(self):
        """
        Devuelve el string que identifica a cada paciente.

        Return :
        --------
            str : string que representa un paciente.
        """

        return f"ID: {self.IDPac}, Tipo de Consulta: {self.consulta}, Urgencia: {self.urgencia}, Tiempo Estimado: {self.tEstimado}"
    