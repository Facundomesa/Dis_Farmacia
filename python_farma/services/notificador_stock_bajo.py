import threading
import queue
import time
from python_farma.entidades.producto import Producto

# El evento que recibe de la cola
TipoEventoStock = tuple[Producto, int]

class NotificadorStockBajo(threading.Thread):
    
    def __init__(
        self, 
        cola_eventos: queue.Queue[TipoEventoStock],
        email_destino: str
    ):
        """
        Inicializa el hilo consumidor.
        
        Args:
            cola_eventos: La cola (Queue) de la que consumirá eventos.
            email_destino: Email al que se enviarán las alertas.
        """
        # Configura el hilo como "daemon" (rúbrica 5.1)
        super().__init__(daemon=True, name="NotificadorStockBajoThread")
        
        self._cola_eventos = cola_eventos
        self._email_destino = email_destino
        # Event para "Graceful Shutdown" (rúbrica 4.2)
        self._stop_event = threading.Event()

    def run(self):
        """
        Método principal del hilo (se llama con .start()).
        Contiene el bucle de consumo de eventos.
        """
        print(f"[Notificador Hilo] Hilo iniciado. Monitoreando cola de eventos...")
        
        while not self._stop_event.is_set():
            try:
                # Espera un evento en la cola (con timeout)
                # El timeout es crucial para que el bucle
                # pueda verificar _stop_event periódicamente.
                evento = self._cola_eventos.get(timeout=1.0)
                
                # Si llegamos aquí, tenemos un evento
                producto, nuevo_stock = evento
                
                print(f"[Notificador Hilo] Evento recibido: "
                      f"Producto '{producto.nombre}', Stock: {nuevo_stock}")
                
                # Lógica del notificador:
                if nuevo_stock < producto.umbral_minimo:
                    self._enviar_alerta_stock_bajo(producto)
                    
                # Marcamos la tarea como completada en la cola
                self._cola_eventos.task_done()
                
            except queue.Empty:
                # Esto es normal. El timeout de 1.0s expiró.
                # El bucle vuelve a empezar y revisa _stop_event.
                continue
                
        print("[Notificador Hilo] Hilo detenido limpiamente.")

    def _enviar_alerta_stock_bajo(self, producto: Producto):
        """
        Simula el envío de un email de alerta.
        (En un hilo separado, no bloquea la venta)
        """
        print("\n" + "="*30)
        print(f"!!! ALERTA DE STOCK BAJO (ASINC) !!!")
        print(f"Enviando email a: {self._email_destino}")
        print(f"Asunto: Stock bajo para {producto.nombre}")
        print(f"Mensaje: El producto '{producto.nombre}' "
              f"ha alcanzado {producto.stock} unidades "
              f"(Umbral: {producto.umbral_minimo}).")
        print("="*30 + "\n")
        
        # Simulamos que enviar el email toma tiempo
        time.sleep(1) 

    def detener(self):
        """
        Señaliza al hilo que debe detenerse (Graceful Shutdown).
        """
        print("[Notificador Hilo] Señal de detención recibida...")
        self._stop_event.set()