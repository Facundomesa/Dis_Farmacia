from typing import List, Dict
from python_farma.entidades.producto import Producto
from python_farma.patrones.observer.observable import Observable
from python_farma.patrones.factory.producto_factory import ProductoFactory
from python_farma.excepciones.stock_insuficiente_excepcion import StockInsuficienteException

# El evento que notificamos es un tuple: (Producto, nuevo_stock_int)
TipoEventoStock = tuple[Producto, int]

class InventarioService(Observable[TipoEventoStock]):
    """
    Gestiona el inventario de productos.
    Es un Observable que notifica a los Observadores (ej. NotificadorStockBajo)
    cuando el stock de un producto cambia.
    """
    
    def __init__(self):
        super().__init__()
        # Usamos un diccionario para acceso rápido por nombre
        self._productos: Dict[str, Producto] = {}

    def crear_producto(
        self, 
        tipo_producto: str, 
        nombre: str, 
        precio_base: float,
        stock_inicial: int
    ) -> Producto:
        """
        Crea un producto usando la Factory y lo añade al inventario.
        """
        # Delega la creación a la Factory
        producto = ProductoFactory.crear_producto(
            tipo_producto, nombre, precio_base, stock_inicial
        )
        
        if producto.nombre in self._productos:
            raise ValueError(f"El producto '{producto.nombre}' ya existe.")
            
        self._productos[producto.nombre] = producto
        return producto

    def get_producto(self, nombre: str) -> Producto:
        """Obtiene un producto por nombre."""
        producto = self._productos.get(nombre)
        if not producto:
            raise ValueError(f"Producto no encontrado: {nombre}")
        return producto

    def descontar_stock(self, nombre_producto: str, cantidad: int):
        """
        Descuenta el stock de un producto y notifica a los observadores.
        Este es el método clave que dispara el Patrón Observer.
        """
        producto = self.get_producto(nombre_producto)
        
        try:
            # Intenta descontar el stock en la entidad
            producto.descontar_stock(cantidad)
            
            print(f"[Inventario] Stock descontado. Producto: '{producto.nombre}', "
                  f"Stock restante: {producto.stock}")
            
            # --- Disparador del Patrón Observer ---
            # Notifica a todos los observadores sobre el cambio.
            # Enviamos el objeto producto y su nuevo stock.
            evento: TipoEventoStock = (producto, producto.stock)
            self.notificar_observadores(evento)
            # ----------------------------------------
            
        except ValueError as e:
            # Captura el error de la entidad y lo relanza como excepción de servicio
            raise StockInsuficienteException(
                producto_nombre=nombre_producto,
                stock_requerido=cantidad,
                stock_disponible=producto.stock
            ) from e