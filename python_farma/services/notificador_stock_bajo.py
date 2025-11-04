from python_farma.patrones.observer.observer import Observer
from python_farma.entidades.producto import Producto

# El evento que recibe es el definido en InventarioService
TipoEventoStock = tuple[Producto, int]

class NotificadorStockBajo(Observer[TipoEventoStock]):
    """
    Observador que comprueba si el stock ha caído por debajo 
    del umbral mínimo y envía una alerta.
    """
    
    def __init__(self, email_destino: str):
        self._email_destino = email_destino

    def actualizar(self, evento: TipoEventoStock) -> None:
        """
        Método de actualización (callback) llamado por el Observable.
        Implementación del Patrón Observer.
        """
        producto, nuevo_stock = evento
        
        print(f"[Observer] Notificador ha recibido actualización: "
              f"Producto '{producto.nombre}', Stock: {nuevo_stock}")
        
        # Lógica del observador:
        if nuevo_stock < producto.umbral_minimo:
            self._enviar_alerta_stock_bajo(producto)

    def _enviar_alerta_stock_bajo(self, producto: Producto):
        """Simula el envío de un email de alerta."""
        print("\n" + "="*30)
        print(f"!!! ALERTA DE STOCK BAJO !!!")
        print(f"Enviando email a: {self._email_destino}")
        print(f"Asunto: Stock bajo para {producto.nombre}")
        print(f"Mensaje: El producto '{producto.nombre}' "
              f"ha alcanzado {producto.stock} unidades "
              f"(Umbral: {producto.umbral_minimo}).")
        print("="*30 + "\n")