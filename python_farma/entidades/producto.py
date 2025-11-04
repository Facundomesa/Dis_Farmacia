from abc import ABC, abstractmethod
from python_farma.constantes import UMBRAL_MINIMO_STOCK_GENERAL

class Producto(ABC):
    """
    Clase base para todos los productos de la farmacia.
    Contiene los atributos y lógica comunes.
    """
    def __init__(self, nombre: str, precio_base: float, stock: int):
        if precio_base <= 0:
            raise ValueError("El precio base debe ser positivo.")
        if stock < 0:
            raise ValueError("El stock no puede ser negativo.")
            
        self._nombre = nombre
        self._precio_base = precio_base
        self._stock = stock
        # Define un umbral de stock genérico
        self._umbral_minimo = UMBRAL_MINIMO_STOCK_GENERAL

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def precio_base(self) -> float:
        return self._precio_base

    @property
    def stock(self) -> int:
        return self._stock

    @property
    def umbral_minimo(self) -> int:
        return self._umbral_minimo

    def descontar_stock(self, cantidad: int) -> None:
        """Reduce el stock del producto."""
        if cantidad <= 0:
            raise ValueError("La cantidad a descontar debe ser positiva.")
        if (self._stock - cantidad) < 0:
            # Esta excepción será capturada por el servicio
            raise ValueError(f"Stock insuficiente para {self._nombre}")
        self._stock -= cantidad

    @abstractmethod
    def get_tipo_producto(self) -> str:
        """Método abstracto para identificar el tipo de producto."""
        pass