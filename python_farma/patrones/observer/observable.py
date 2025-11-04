import threading
from typing import Generic, TypeVar, List
from abc import ABC
from python_farma.patrones.observer.observer import Observer

# Tipo genérico para el evento/dato que se notifica
T = TypeVar('T')

class Observable(Generic[T], ABC):
    """
    La clase base Observable (Sujeto) maneja la suscripción 
    y notificación de observadores.
    """
    
    def __init__(self):
        self._observadores: List[Observer[T]] = []
        self._lock = threading.Lock() # Para seguridad en hilos

    def agregar_observador(self, observador: Observer[T]) -> None:
        """Agrega un observador a la lista."""
        with self._lock:
            if observador not in self._observadores:
                self._observadores.append(observador)

    def eliminar_observador(self, observador: Observer[T]) -> None:
        """Elimina un observador de la lista."""
        with self._lock:
            try:
                self._observadores.remove(observador)
            except ValueError:
                pass # No hacer nada si el observador no estaba

    def notificar_observadores(self, evento: T) -> None:
        """Notifica a todos los observadores suscritos."""
        with self._lock:
            # Iteramos sobre una copia por si la lista es modificada
            # por un observador durante la notificación.
            for observador in self._observadores[:]:
                observador.actualizar(evento)