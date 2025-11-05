"""
Archivo integrador generado automaticamente
Directorio: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\python_farma\excepciones
Fecha: 2025-11-05 10:11:11
Total de archivos integrados: 4
"""

# ================================================================================
# ARCHIVO 1/4: __init__.py
# Ruta: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\python_farma\excepciones\__init__.py
# ================================================================================



# ================================================================================
# ARCHIVO 2/4: farmacia_excepcion.py
# Ruta: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\python_farma\excepciones\farmacia_excepcion.py
# ================================================================================

class FarmaciaException(Exception):
    """Excepción base para errores de la aplicación."""
    def __init__(self, mensaje: str):
        self.mensaje = mensaje
        super().__init__(self.mensaje)

# ================================================================================
# ARCHIVO 3/4: persistencia_excepcion.py
# Ruta: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\python_farma\excepciones\persistencia_excepcion.py
# ================================================================================

from python_farma.excepciones.farmacia_excepcion import FarmaciaException

class PersistenciaException(FarmaciaException):
    """Lanzada cuando falla una operación de serialización (pickle) o I/O."""
    
    def __init__(self, mensaje: str, error_original: Exception | None = None):
        self.error_original = error_original
        mensaje_completo = f"Error de persistencia: {mensaje}"
        if error_original:
            mensaje_completo += f". Error base: {error_original}"
            
        super().__init__(mensaje_completo)

# ================================================================================
# ARCHIVO 4/4: stock_insuficiente_excepcion.py
# Ruta: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\python_farma\excepciones\stock_insuficiente_excepcion.py
# ================================================================================

from python_farma.excepciones.farmacia_excepcion import FarmaciaException

class StockInsuficienteException(FarmaciaException):
    """Lanzada cuando se intenta vender más stock del disponible."""
    def __init__(
        self, 
        producto_nombre: str, 
        stock_requerido: int, 
        stock_disponible: int
    ):
        self.producto_nombre = producto_nombre
        self.stock_requerido = stock_requerido
        self.stock_disponible = stock_disponible
        mensaje = (
            f"Stock insuficiente para '{producto_nombre}'. "
            f"Requerido: {stock_requerido}, Disponible: {stock_disponible}"
        )
        super().__init__(mensaje)

