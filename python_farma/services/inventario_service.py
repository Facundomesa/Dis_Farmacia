import queue
from typing import List, Dict
from python_farma.entidades.producto import Producto
from python_farma.patrones.factory.producto_factory import ProductoFactory
from python_farma.excepciones.stock_insuficiente_excepcion import StockInsuficienteException

# El evento que ponemos en la cola: (Producto, nuevo_stock_int)
TipoEventoStock = tuple[Producto, int]

class InventarioService:
    """
    Gestiona el inventario de productos.
    Es un Productor: Pone eventos de stock en una cola para
    que los Consumidores (Notificadores) los procesen asincrónicamente.
    """
    
    def __init__(self, cola_eventos_stock: queue.Queue[TipoEventoStock]):
        """
        Inicializa el servicio de inventario.
        
        Args:
            cola_eventos_stock: La cola (Queue) donde se pondrán los
                                eventos de cambio de stock.
        """
        self._productos: Dict[str, Producto] = {}
        # Recibe la cola por Inyección de Dependencias
        self._cola_eventos = cola_eventos_stock

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
        Descuenta el stock de un producto y COLOCA el evento en la cola.
        Este es el disparador del patrón Productor-Consumidor.
        """
        producto = self.get_producto(nombre_producto)
        
        try:
            # Intenta descontar el stock en la entidad
            producto.descontar_stock(cantidad)
            
            print(f"[Inventario] Stock descontado. Producto: '{producto.nombre}', "
                  f"Stock restante: {producto.stock}")
            
            # --- Disparador del Patrón (ASINCRÓNICO) ---
            # Pone el evento en la cola.
            # Esto es instantáneo y no bloquea la venta.
            evento: TipoEventoStock = (producto, producto.stock)
            self._cola_eventos.put(evento)
            # ----------------------------------------
            
        except ValueError as e:
            # Captura el error de la entidad y lo relanza como excepción de servicio
            raise StockInsuficienteException(
                producto_nombre=nombre_producto,
                stock_requerido=cantidad,
                stock_disponible=producto.stock
            ) from e

    # --- MÉTODO NUEVO (OPCIÓN 3) ---
    def get_todos_los_productos(self) -> List[Producto]:
        return list(self._productos.values())