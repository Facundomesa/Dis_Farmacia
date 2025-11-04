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