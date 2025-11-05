"""
Archivo integrador generado automaticamente
Directorio: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\python_farma\patrones\observer
Fecha: 2025-11-05 10:11:11
Total de archivos integrados: 3
"""

# ================================================================================
# ARCHIVO 1/3: __init__.py
# Ruta: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\python_farma\patrones\observer\__init__.py
# ================================================================================



# ================================================================================
# ARCHIVO 2/3: observable.py
# Ruta: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\python_farma\patrones\observer\observable.py
# ================================================================================

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

# ================================================================================
# ARCHIVO 3/3: observer.py
# Ruta: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\python_farma\patrones\observer\observer.py
# ================================================================================

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

