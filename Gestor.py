import array_queue
import Paciente

class Gestor :
    def __init__(self, GeneralUrgente, GeneralNoUrgente, EspecificoUrgente, EspecificoNoUrgente, Admision):
        self._GeneralUrgente = GeneralUrgente
        self._GeneralNoUrgente = GeneralNoUrgente
        self._EspecificoUrgente = EspecificoUrgente
        self._EspecificoNoUrgente = EspecificoNoUrgente
        self._Admision = Admision

    @property
    def GeneralUrgente(self) :
        return self._GeneralUrgente
    
    @GeneralUrgente.setter
    def GeneralUrgente(self) :
        if all(pacientes.consulta == 'General' for pacientes in self.GeneralUrgente) and all(pacientes.urgencia for pacientes in self.GeneralUrgente ) :
            return self._GeneralUrgente
        else :
            raise TypeError('Los pacientes no pertenecen a la cola de atención general urgente.')
    
    @property
    def GeneralNoUrgente(self) :
        return self._GeneralNoUrgente
    
    @GeneralNoUrgente.setter
    def GeneralNoUrgente(self, cola: array_queue) :
        if all(pacientes.consulta == 'General' for pacientes in self.GeneralNoUrgente) and all(not pacientes.urgencia for pacientes in self.GeneralNoUrgente ) :
            return self._GeneralNoUrgente
        else :
            raise TypeError('Los pacientes no pertenecen a la cola de atención general no urgente.')
    