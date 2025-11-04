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

# --- NUEVA CLASE (OPCIÓN 3) ---
class SuplementoDietario(Producto):
    """Producto tipo Suplemento Dietario."""
    def __init__(self, nombre: str, precio_base: float, stock: int):
        super().__init__(nombre, precio_base, stock)
        self._requiere_consulta = False
        
    def get_tipo_producto(self) -> str:
        return "SuplementoDietario"