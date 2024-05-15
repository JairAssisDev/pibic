from abc import ABC, abstractmethod

class PacienteService(ABC):
    @abstractmethod
    def criar_paciente(self, dados_paciente):
        pass

    @abstractmethod
    def obter_todos_pacientes(self):
        pass

    @abstractmethod
    def obter_paciente_por_nome(self, nome):
        pass
