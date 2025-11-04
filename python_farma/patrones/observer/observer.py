from typing import Generic, TypeVar, Any
from abc import ABC, abstractmethod

# Tipo genérico para el evento/dato que se notifica
T = TypeVar('T')

class Observer(Generic[T], ABC):
    """
    La interfaz Observer declara el método de actualización (actualizar), 
    utilizado por los Sujetos (Observables).
    """
    
    @abstractmethod
    def actualizar(self, evento: T) -> None:
        """
        Recibe la actualización desde el sujeto.
        
        Args:
            evento: El dato/evento notificado por el sujeto.
        """
        pass