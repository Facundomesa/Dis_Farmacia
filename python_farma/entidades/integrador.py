"""
Archivo integrador generado automaticamente
Directorio: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\python_farma\entidades
Fecha: 2025-11-05 10:11:11
Total de archivos integrados: 4
"""

# ================================================================================
# ARCHIVO 1/4: __init__.py
# Ruta: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\python_farma\entidades\__init__.py
# ================================================================================



# ================================================================================
# ARCHIVO 2/4: cliente.py
# Ruta: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\python_farma\entidades\cliente.py
# ================================================================================

class Cliente:
    """Almacena datos de un cliente."""
    
    def __init__(self, dni: str, nombre: str, es_jubilado: bool = False):
        self._dni = dni
        self._nombre = nombre
        self._es_jubilado = es_jubilado
        self._obra_social: str | None = None

    @property
    def dni(self) -> str:
        return self._dni
        
    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def es_jubilado(self) -> bool:
        return self._es_jubilado

    def __str__(self) -> str:
        """Representación en string para fácil debugging."""
        jubilado_str = "Sí" if self._es_jubilado else "No"
        return f"Cliente [DNI: {self._dni}, Nombre: {self._nombre}, Jubilado: {jubilado_str}]"

# ================================================================================
# ARCHIVO 3/4: producto.py
# Ruta: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\python_farma\entidades\producto.py
# ================================================================================

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

# ================================================================================
# ARCHIVO 4/4: tipos_producto.py
# Ruta: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\python_farma\entidades\tipos_producto.py
# ================================================================================

from python_farma.entidades.producto import Producto
from python_farma.constantes import UMBRAL_MINIMO_STOCK_MEDICAMENTOS

class MedicamentoConReceta(Producto):
    """Producto tipo Medicamento que requiere receta."""
    def __init__(self, nombre: str, precio_base: float, stock: int):
        super().__init__(nombre, precio_base, stock)
        self._receta_requerida = True
        # Los medicamentos tienen un umbral de stock más sensible
        self._umbral_minimo = UMBRAL_MINIMO_STOCK_MEDICAMENTOS
        
    def get_tipo_producto(self) -> str:
        return "MedicamentoConReceta"

class MedicamentoOTC(Producto):
    """Producto tipo Medicamento de Venta Libre (Over-The-Counter)."""
    def __init__(self, nombre: str, precio_base: float, stock: int):
        super().__init__(nombre, precio_base, stock)
        self._receta_requerida = False
        self._umbral_minimo = UMBRAL_MINIMO_STOCK_MEDICAMENTOS
        
    def get_tipo_producto(self) -> str:
        return "MedicamentoOTC"

class Perfumeria(Producto):
    """Producto tipo Perfumería."""
    def __init__(self, nombre: str, precio_base: float, stock: int):
        super().__init__(nombre, precio_base, stock)
        self._descuento_promocion: float = 0.1 # Ej. 10% promo
        
    def get_tipo_producto(self) -> str:
        return "Perfumeria"

    @property
    def descuento_promocion(self) -> float:
        return self._descuento_promocion


class SuplementoDietario(Producto):
    """Producto tipo Suplemento Dietario."""
    def __init__(self, nombre: str, precio_base: float, stock: int):
        super().__init__(nombre, precio_base, stock)
        self._requiere_consulta = False
        
    def get_tipo_producto(self) -> str:
        return "SuplementoDietario"

