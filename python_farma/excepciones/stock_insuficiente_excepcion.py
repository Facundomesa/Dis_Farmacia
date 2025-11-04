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