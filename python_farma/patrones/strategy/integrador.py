"""
Archivo integrador generado automaticamente
Directorio: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\python_farma\patrones\strategy
Fecha: 2025-11-05 10:11:11
Total de archivos integrados: 2
"""

# ================================================================================
# ARCHIVO 1/2: __init__.py
# Ruta: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\python_farma\patrones\strategy\__init__.py
# ================================================================================



# ================================================================================
# ARCHIVO 2/2: i_estrategia_descuento.py
# Ruta: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\python_farma\patrones\strategy\i_estrategia_descuento.py
# ================================================================================

from abc import ABC, abstractmethod

class IEstrategiaDescuento(ABC):
    """
    Interfaz común para todas las estrategias de cálculo de descuento.
    """
    
    @abstractmethod
    def calcular_descuento(self, monto_total: float) -> float:
        """
        Calcula el descuento a aplicar sobre un monto total.
        
        Args:
            monto_total: El subtotal de la venta.
            
        Returns:
            El monto del descuento (no el precio final).
        """
        pass

