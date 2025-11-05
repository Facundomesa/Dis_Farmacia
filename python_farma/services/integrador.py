"""
Archivo integrador generado automaticamente
Directorio: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\python_farma\services
Fecha: 2025-11-05 10:11:11
Total de archivos integrados: 5
"""

# ================================================================================
# ARCHIVO 1/5: __init__.py
# Ruta: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\python_farma\services\__init__.py
# ================================================================================



# ================================================================================
# ARCHIVO 2/5: inventario_service.py
# Ruta: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\python_farma\services\inventario_service.py
# ================================================================================

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

# ================================================================================
# ARCHIVO 3/5: notificador_stock_bajo.py
# Ruta: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\python_farma\services\notificador_stock_bajo.py
# ================================================================================

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

# ================================================================================
# ARCHIVO 4/5: persistencia_service.py
# Ruta: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\python_farma\services\persistencia_service.py
# ================================================================================

import pickle
import os
from python_farma.entidades.cliente import Cliente
from python_farma.excepciones.persistencia_excepcion import PersistenciaException

# Directorio donde se guardarán los datos
_DATA_DIR = "data"
# Extensión para nuestros archivos de datos
_DATA_EXT = ".dat"

class PersistenciaService:
    """Gestiona el guardado y lectura de entidades."""
    
    def __init__(self):
        self._crear_directorio_data()
        
    def _crear_directorio_data(self):
        """Crea el directorio 'data' si no existe."""
        try:
            os.makedirs(_DATA_DIR, exist_ok=True)
        except OSError as e:
            raise PersistenciaException(f"No se pudo crear el directorio '{_DATA_DIR}'", e)

    def _get_ruta_archivo(self, id_objeto: str) -> str:
        """Genera la ruta completa del archivo para un objeto."""
        return os.path.join(_DATA_DIR, f"cliente_{id_objeto}{_DATA_EXT}")
        
    def guardar_cliente(self, cliente: Cliente):
        """
        Guarda un objeto Cliente en disco usando Pickle.
        El nombre del archivo será 'cliente_[DNI].dat'.
        """
        ruta_archivo = self._get_ruta_archivo(cliente.dni)
        print(f"[Persistencia] Guardando cliente en '{ruta_archivo}'...")
        
        try:
            with open(ruta_archivo, "wb") as f:
                pickle.dump(cliente, f)
            print(f"[Persistencia] Cliente DNI {cliente.dni} guardado exitosamente.")
            
        except (IOError, pickle.PickleError) as e:
            raise PersistenciaException(f"No se pudo guardar el archivo {ruta_archivo}", e)

    def leer_cliente(self, dni: str) -> Cliente:
        """
        Lee un objeto Cliente desde disco usando Pickle.
        
        Raises:
            PersistenciaException si el archivo no existe o está corrupto.
        """
        ruta_archivo = self._get_ruta_archivo(dni)
        print(f"[Persistencia] Leyendo cliente desde '{ruta_archivo}'...")
        
        if not os.path.exists(ruta_archivo):
            raise PersistenciaException(f"Archivo no encontrado: {ruta_archivo}", FileNotFoundError())

        try:
            with open(ruta_archivo, "rb") as f:
                cliente = pickle.load(f)
                
            if not isinstance(cliente, Cliente):
                raise PersistenciaException(f"El archivo {ruta_archivo} no contiene un Cliente válido.")
                
            print(f"[Persistencia] Cliente DNI {dni} leído exitosamente.")
            return cliente
            
        except (IOError, pickle.PickleError, EOFError) as e:
            raise PersistenciaException(f"No se pudo leer o deserializar el archivo {ruta_archivo}", e)

# ================================================================================
# ARCHIVO 5/5: venta_service.py
# Ruta: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\python_farma\services\venta_service.py
# ================================================================================

from typing import List, Optional
from python_farma.entidades.producto import Producto
from python_farma.patrones.strategy.i_estrategia_descuento import IEstrategiaDescuento
from python_farma.patrones.strategy.implementacion.estrategias_descuento import EstrategiaSinDescuento
from python_farma.config.configuracion import ConfiguracionSistema

# Simulación de un carrito de compras
TipoCarrito = List[Producto]

class VentaService:
    """
    Gestiona el proceso de venta.
    Es el Contexto del Patrón Strategy.
    """
    
    def __init__(self):
        # Inyecta la configuración (Singleton)
        self._config = ConfiguracionSistema.get_instance()
        
        # Inicia con una estrategia por defecto (nula)
        self._estrategia_descuento: IEstrategiaDescuento = EstrategiaSinDescuento()
        
        print("[VentaService] Creado. Usando Singleton Config.")
        print(f"[VentaService] Tasa de IVA obtenida: {self._config.get_tasa_iva()}")

    def set_estrategia(self, estrategia: IEstrategiaDescuento):
        """
        Permite al cliente cambiar la estrategia en tiempo de ejecución.
        (Inyección de dependencia por Setter)
        """
        print(f"[Strategy] VentaService: Cambiando a estrategia '{estrategia.__class__.__name__}'")
        self._estrategia_descuento = estrategia

    def calcular_total_venta(self, carrito: TipoCarrito) -> float:
        """
        Calcula el total de la venta aplicando la estrategia actual.
        """
        # 1. Calcular Subtotal
        subtotal = sum(producto.precio_base for producto in carrito)
        print(f"\n[Venta] Calculando total. Subtotal: ${subtotal:.2f}")

        # 2. Calcular Descuento (Delegación al Patrón Strategy)
        descuento = self._estrategia_descuento.calcular_descuento(subtotal)
        
        # 3. Calcular Impuestos (Uso del Patrón Singleton)
        tasa_iva = self._config.get_tasa_iva()
        subtotal_con_dto = subtotal - descuento
        iva = subtotal_con_dto * tasa_iva
        
        # 4. Calcular Total Final
        total_final = subtotal_con_dto + iva

        print(f"[Venta] Descuento: ${descuento:.2f}")
        print(f"[Venta] IVA ({tasa_iva*100}%): ${iva:.2f}")
        print(f"[Venta] TOTAL VENTA: ${total_final:.2f}")
        return total_final

