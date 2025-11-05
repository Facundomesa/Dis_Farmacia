"""
INTEGRADOR FINAL - CONSOLIDACION COMPLETA DEL PROYECTO
============================================================================
Proyecto: PythonFarma
Directorio raiz: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\python_farma
Fecha de generacion: 2025-11-05 09:52:58
Total de archivos integrados: 30
Total de directorios procesados: 12
============================================================================
"""

# ==============================================================================
# TABLA DE CONTENIDOS
# ==============================================================================

# DIRECTORIO: ..
#   1. main.py
#
# DIRECTORIO: .
#   1. __init__.py
#   2. constantes.py
#
# DIRECTORIO: config
#   3. __init__.py
#   4. configuracion.py
#
# DIRECTORIO: entidades
#   5. __init__.py
#   6. cliente.py
#   7. producto.py
#   8. tipos_producto.py
#
# DIRECTORIO: excepciones
#   9. __init__.py
#   10. farmacia_excepcion.py
#   11. persistencia_excepcion.py
#   12. stock_insuficiente_excepcion.py
#
# DIRECTORIO: patrones
#   13. __init__.py
#
# DIRECTORIO: patrones\factory
#   14. __init__.py
#   15. producto_factory.py
#
# DIRECTORIO: patrones\observer
#   16. __init__.py
#   17. observable.py
#   18. observer.py
#
# DIRECTORIO: patrones\registry
#   19. __init__.py
#   20. registros_servicios.py
#
# DIRECTORIO: patrones\strategy
#   21. __init__.py
#   22. i_estrategia_descuento.py
#
# DIRECTORIO: patrones\strategy\implementacion
#   23. __init__.py
#   24. estrategias_descuento.py
#
# DIRECTORIO: services
#   25. __init__.py
#   26. inventario_service.py
#   27. notificador_stock_bajo.py
#   28. persistencia_service.py
#   29. venta_service.py
#



################################################################################
# DIRECTORIO: ..
################################################################################

# ==============================================================================
# ARCHIVO 1/30: main.py
# Directorio: ..
# Ruta completa: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\main.py
# ==============================================================================

import queue
import time
from python_farma.config.configuracion import ConfiguracionSistema
from python_farma.patrones.registry.registros_servicios import RegistroServicios
from python_farma.services.inventario_service import InventarioService, TipoEventoStock
from python_farma.services.notificador_stock_bajo import NotificadorStockBajo
from python_farma.services.venta_service import VentaService
from python_farma.services.persistencia_service import PersistenciaService
from python_farma.entidades.cliente import Cliente
from python_farma.patrones.strategy.implementacion.estrategias_descuento import (
    EstrategiaDescuentoJubilado,
    EstrategiaSinDescuento
)
from python_farma.excepciones.stock_insuficiente_excepcion import StockInsuficienteException
from python_farma.excepciones.persistencia_excepcion import PersistenciaException


# --- Clases de servicio simuladas para el Registry ---
class LoggerServicio:
    def info(self, mensaje: str):
        print(f"[Logger] {mensaje}")

class DBManager:
    def __init__(self, host: str):
        self._host = host
        print(f"[DBManager] Conectado a {self._host}")
# ----------------------------------------------------


def demonstrate_singleton_and_registry():
    """Demuestra Singleton y Registry."""
    print("\n--- 1. DEMO SINGLETON Y REGISTRY ---")
    
    # --- Singleton ---
    config = ConfiguracionSistema.get_instance()
    
    # --- Registry ---
    registro = RegistroServicios.get_instance()
    
    # Registramos servicios
    registro.registrar_servicio("logger", LoggerServicio())
    registro.registrar_servicio("db_manager", DBManager(config.get_db_host()))

    # Usamos un servicio del Registry
    logger = registro.get_servicio("logger")
    logger.info("Demostración de Singleton y Registry completada.")

    # Verificamos que Singleton es la misma instancia
    config2 = ConfiguracionSistema.get_instance()
    assert config is config2, "Error: Singleton falló, las instancias son diferentes."
    print("[OK] Singleton verificado (misma instancia).")


def demonstrate_factory_and_observer_async(
    inventario_service: InventarioService
) -> InventarioService:
    """Demuestra Factory (4 productos) y Observer (Asincrónico)."""
    print("\n--- 2. DEMO FACTORY (4 PRODUCTOS) Y OBSERVER (ASINC) ---")
    
    # --- Factory ---
    # Usamos el servicio de inventario, que USA la Factory internamente.
    print("\n[Factory] Creando 4 tipos de productos...")
    try:
        inventario_service.crear_producto(
            tipo_producto="Perfumeria",
            nombre="Perfume 'Olympea'",
            precio_base=35000.0,
            stock_inicial=15
        )
        
        inventario_service.crear_producto(
            tipo_producto="MedicamentoConReceta",
            nombre="Amoxicilina 500mg",
            precio_base=1500.0,
            stock_inicial=12 # Stock inicial bajo (umbral es 10)
        )
        
        inventario_service.crear_producto(
            tipo_producto="MedicamentoOTC",
            nombre="Ibuprofeno 400mg",
            precio_base=800.0,
            stock_inicial=50
        )
        
    
        inventario_service.crear_producto(
            tipo_producto="SuplementoDietario",
            nombre="Proteína Whey",
            precio_base=12000.0,
            stock_inicial=20
        )
        print("[OK] Factory creó 4 tipos de productos.")
        
    except ValueError as e:
        print(f"[Error] Falló la creación de producto: {e}")

    # --- Disparar Observer (Asincrónico) ---
    # Simulamos una venta que reduce el stock de Amoxicilina
    # Esto debería poner el evento en la cola y el HILO notificador lo procesará.
    print("\n[Observer] Simulando venta que dispara alerta de stock (asinc)...")
    try:
        # El umbral es 10. Al descontar 3, el stock queda en 9.
        inventario_service.descontar_stock(
            nombre_producto="Amoxicilina 500mg", 
            cantidad=3
        )
        print("[Venta] Venta completada. El hilo notificador procesará la alerta.")
    except StockInsuficienteException as e:
        print(f"[Error Venta] {e.mensaje}")
    
    return inventario_service

def demonstrate_strategy(inventario: InventarioService):
    """Demuestra el Patrón Strategy."""
    print("\n--- 3. DEMO STRATEGY (PUNTO DE VENTA) ---")
    
    # --- Preparación ---
    venta_service = VentaService()
    
    try:
        perfume = inventario.get_producto("Perfume 'Olympea'")
        ibuprofeno = inventario.get_producto("Ibuprofeno 400mg")
    except ValueError as e:
        print(f"Error fatal: No se pudieron recuperar productos: {e}")
        return

    # --- Venta 1: Cliente Regular (Sin Descuento) ---
    print("\n[Strategy] PROCESANDO VENTA 1 (Cliente Regular)")
    carrito_1 = [perfume, ibuprofeno]
    venta_service.set_estrategia(EstrategiaSinDescuento())
    venta_service.calcular_total_venta(carrito_1)

    # --- Venta 2: Cliente Jubilado (Con Descuento) ---
    print("\n[Strategy] PROCESANDO VENTA 2 (Cliente Jubilado)")
    carrito_2 = [inventario.get_producto("Amoxicilina 500mg")]
    venta_service.set_estrategia(EstrategiaDescuentoJubilado())
    venta_service.calcular_total_venta(carrito_2)

def demonstrate_persistence():
    """Demuestra el servicio de Persistencia con Pickle."""
    print("\n--- 4. DEMO PERSISTENCIA (PICKLE) ---")
    
    persistencia_service = PersistenciaService()
    cliente_nuevo = Cliente(dni="12345678", nombre="Juan Perez", es_jubilado=True)
    
    # 1. Guardar
    try:
        persistencia_service.guardar_cliente(cliente_nuevo)
    except PersistenciaException as e:
        print(f"[Error] Falló al guardar: {e}")
        return

    # 2. Leer
    try:
        cliente_leido = persistencia_service.leer_cliente("12345678")
        print(f"[Persistencia] Cliente recuperado: {cliente_leido}")
        
        # Verificación
        assert cliente_nuevo.dni == cliente_leido.dni
        assert cliente_nuevo.nombre == cliente_leido.nombre
        print("[OK] Persistencia verificada (guardado y lectura exitosos).")
        
    except PersistenciaException as e:
        print(f"[Error] Falló al leer: {e}")


def main():
    """Punto de entrada principal de la aplicación."""
    print("="*60)
    print("     SISTEMA DE GESTIÓN DE FARMACIA (PythonFarma)")
    print("     Demostración de Patrones de Diseño (Versión Avanzada)")
    print("="*60)
    
    # 1. Crear la cola de comunicación
    cola_eventos_stock: queue.Queue[TipoEventoStock] = queue.Queue()
    
    # 2. Crear el Hilo Consumidor (Notificador)
    email_compras = "compras@pythonfarma.com"
    notificador_compras = NotificadorStockBajo(cola_eventos_stock, email_compras)
    
    # 3. Iniciar el Hilo Consumidor (¡Importante!)
    notificador_compras.start()
    # ---------------------------------------------------------
    
    # 4. Crear el Productor (Inventario) y le pasamos la cola
    inventario_service = InventarioService(cola_eventos_stock=cola_eventos_stock)

    
    # Demo 1: Singleton y Registry
    demonstrate_singleton_and_registry()
    
    # Demo 2: Factory y Observer (Asincrónico)
    demonstrate_factory_and_observer_async(inventario_service)
    
    # Demo 3: Strategy
    demonstrate_strategy(inventario_service)
    
    # Demo 4: Persistencia
    demonstrate_persistence()

    # --- Apagado Limpio (Graceful Shutdown) ---
    print("\n" + "="*60)
    print("     DEMOSTRACIÓN FINALIZADA")
    print("="*60)

    print("[Main] Esperando 2 segundos para que el hilo procese la alerta...")
    time.sleep(2) # Dar tiempo al hilo notificador de procesar el evento
    
    print("[Main] Enviando señal de detención al hilo Notificador...")
    notificador_compras.detener()
    
    notificador_compras.join(timeout=3.0) 
    print("[Main] Hilo Notificador detenido. Saliendo.")

    print("\nResumen de Patrones y Funcionalidades:")
    print("[OK] SINGLETON, REGISTRY, FACTORY, STRATEGY")
    print("[OK] OBSERVER (ASINC) con Threading, Queue y Graceful Shutdown.")
    print("[OK] PERSISTENCIA con Pickle y manejo de excepciones.")
    print("[OK] ADICIONALES: 4to Producto y Defensive Copy (implícita).")
    print("="*60)

if __name__ == "__main__":
    main()

################################################################################
# DIRECTORIO: .
################################################################################

# ==============================================================================
# ARCHIVO 2/30: __init__.py
# Directorio: .
# Ruta completa: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\python_farma\__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 3/30: constantes.py
# Directorio: .
# Ruta completa: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\python_farma\constantes.py
# ==============================================================================


# --- Descuentos ---
DTO_JUBILADO = 0.40  # 40%
DTO_OBRA_SOCIAL = 0.20 # 20%
DTO_SIN_DESCUENTO = 0.0 # 0%

# --- Stock ---
UMBRAL_MINIMO_STOCK_MEDICAMENTOS = 10
UMBRAL_MINIMO_STOCK_GENERAL = 5

# --- Impuestos ---
TASA_IVA_GENERAL = 0.21


################################################################################
# DIRECTORIO: config
################################################################################

# ==============================================================================
# ARCHIVO 4/30: __init__.py
# Directorio: config
# Ruta completa: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\python_farma\config\__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 5/30: configuracion.py
# Directorio: config
# Ruta completa: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\python_farma\config\configuracion.py
# ==============================================================================

import threading
from python_farma.constantes import TASA_IVA_GENERAL

class ConfiguracionSistema:
    """
    Clase Singleton que almacena la configuración global.
    Utiliza double-checked locking para ser thread-safe.
    """
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        """Bloquea la instanciación directa."""
        raise TypeError("Clase Singleton. Usar ConfiguracionSistema.get_instance().")

    @classmethod
    def get_instance(cls):
        """
        Método de acceso global a la instancia única.
        """
        if cls._instance is None:
            with cls._lock:  # Primer chequeo (evita lock innecesario)
                if cls._instance is None:  # Segundo chequeo (thread-safe)
                    # Llama a __new__ de la clase base (object)
                    cls._instance = super().__new__(cls)
                    # Inicializa la configuración
                    cls._instance._cargar_configuracion()
        return cls._instance

    def _cargar_configuracion(self):
        """
        Método privado para cargar la configuración.
        Simula la lectura de un archivo .env o .ini.
        """
        print("[Singleton] Cargando configuración desde archivo por única vez...")
        # Valores simulados
        self._tasa_iva = TASA_IVA_GENERAL
        self._cuit = "30-12345678-9"
        self._nombre_farmacia = "PythonFarma"
        self._db_host = "localhost"

    # --- Métodos de acceso a la configuración ---
    
    def get_tasa_iva(self) -> float:
        return self._tasa_iva

    def get_cuit(self) -> str:
        return self._cuit

    def get_db_host(self) -> str:
        return self._db_host


################################################################################
# DIRECTORIO: entidades
################################################################################

# ==============================================================================
# ARCHIVO 6/30: __init__.py
# Directorio: entidades
# Ruta completa: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\python_farma\entidades\__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 7/30: cliente.py
# Directorio: entidades
# Ruta completa: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\python_farma\entidades\cliente.py
# ==============================================================================

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

# ==============================================================================
# ARCHIVO 8/30: producto.py
# Directorio: entidades
# Ruta completa: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\python_farma\entidades\producto.py
# ==============================================================================

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

# ==============================================================================
# ARCHIVO 9/30: tipos_producto.py
# Directorio: entidades
# Ruta completa: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\python_farma\entidades\tipos_producto.py
# ==============================================================================

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


################################################################################
# DIRECTORIO: excepciones
################################################################################

# ==============================================================================
# ARCHIVO 10/30: __init__.py
# Directorio: excepciones
# Ruta completa: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\python_farma\excepciones\__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 11/30: farmacia_excepcion.py
# Directorio: excepciones
# Ruta completa: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\python_farma\excepciones\farmacia_excepcion.py
# ==============================================================================

class FarmaciaException(Exception):
    """Excepción base para errores de la aplicación."""
    def __init__(self, mensaje: str):
        self.mensaje = mensaje
        super().__init__(self.mensaje)

# ==============================================================================
# ARCHIVO 12/30: persistencia_excepcion.py
# Directorio: excepciones
# Ruta completa: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\python_farma\excepciones\persistencia_excepcion.py
# ==============================================================================

from python_farma.excepciones.farmacia_excepcion import FarmaciaException

class PersistenciaException(FarmaciaException):
    """Lanzada cuando falla una operación de serialización (pickle) o I/O."""
    
    def __init__(self, mensaje: str, error_original: Exception | None = None):
        self.error_original = error_original
        mensaje_completo = f"Error de persistencia: {mensaje}"
        if error_original:
            mensaje_completo += f". Error base: {error_original}"
            
        super().__init__(mensaje_completo)

# ==============================================================================
# ARCHIVO 13/30: stock_insuficiente_excepcion.py
# Directorio: excepciones
# Ruta completa: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\python_farma\excepciones\stock_insuficiente_excepcion.py
# ==============================================================================

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


################################################################################
# DIRECTORIO: patrones
################################################################################

# ==============================================================================
# ARCHIVO 14/30: __init__.py
# Directorio: patrones
# Ruta completa: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\python_farma\patrones\__init__.py
# ==============================================================================




################################################################################
# DIRECTORIO: patrones\factory
################################################################################

# ==============================================================================
# ARCHIVO 15/30: __init__.py
# Directorio: patrones\factory
# Ruta completa: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\python_farma\patrones\factory\__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 16/30: producto_factory.py
# Directorio: patrones\factory
# Ruta completa: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\python_farma\patrones\factory\producto_factory.py
# ==============================================================================

from python_farma.entidades import tipos_producto
from python_farma.entidades.producto import Producto

class ProductoFactory:
    """
    Fábrica estática para la creación de diferentes tipos de Producto.
    Desacopla al cliente de las clases concretas.
    """
    
    # Un diccionario (registry) que mapea el tipo (string) a la clase constructora
    _CREADORES = {
        "MedicamentoConReceta": tipos_producto.MedicamentoConReceta,
        "MedicamentoOTC": tipos_producto.MedicamentoOTC,
        "Perfumeria": tipos_producto.Perfumeria,
        "SuplementoDietario": tipos_producto.SuplementoDietario
    }

    @staticmethod
    def crear_producto(
        tipo_producto: str, 
        nombre: str, 
        precio_base: float,
        stock_inicial: int = 100 # Valor por defecto
    ) -> Producto:
        """
        Crea y retorna una instancia de un tipo de Producto.
        
        Args:
            tipo_producto: El string que identifica el tipo a crear.
            nombre: Nombre del producto.
            precio_base: Precio sin IVA.
            stock_inicial: Stock inicial.
            
        Returns:
            Una instancia de una subclase de Producto.
            
        Raises:
            ValueError: Si el tipo_producto no está registrado.
        """
        
        # Obtiene la clase constructora desde el diccionario
        creador = ProductoFactory._CREADORES.get(tipo_producto)
        
        if not creador:
            raise ValueError(f"Tipo de producto desconocido: {tipo_producto}")
            
        # Llama al constructor de la clase concreta (ej. Perfumeria(...))
        print(f"[Factory] Creando producto: '{nombre}' (Tipo: {tipo_producto})")
        return creador(
            nombre=nombre, 
            precio_base=precio_base,
            stock=stock_inicial
        )


################################################################################
# DIRECTORIO: patrones\observer
################################################################################

# ==============================================================================
# ARCHIVO 17/30: __init__.py
# Directorio: patrones\observer
# Ruta completa: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\python_farma\patrones\observer\__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 18/30: observable.py
# Directorio: patrones\observer
# Ruta completa: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\python_farma\patrones\observer\observable.py
# ==============================================================================

import threading
from typing import Generic, TypeVar, List
from abc import ABC
from python_farma.patrones.observer.observer import Observer

# Tipo genérico para el evento/dato que se notifica
T = TypeVar('T')

class Observable(Generic[T], ABC):
    """
    La clase base Observable (Sujeto) maneja la suscripción 
    y notificación de observadores.
    """
    
    def __init__(self):
        self._observadores: List[Observer[T]] = []
        self._lock = threading.Lock() # Para seguridad en hilos

    def agregar_observador(self, observador: Observer[T]) -> None:
        """Agrega un observador a la lista."""
        with self._lock:
            if observador not in self._observadores:
                self._observadores.append(observador)

    def eliminar_observador(self, observador: Observer[T]) -> None:
        """Elimina un observador de la lista."""
        with self._lock:
            try:
                self._observadores.remove(observador)
            except ValueError:
                pass # No hacer nada si el observador no estaba

    def notificar_observadores(self, evento: T) -> None:
        """Notifica a todos los observadores suscritos."""
        with self._lock:
            # Iteramos sobre una copia por si la lista es modificada
            # por un observador durante la notificación.
            for observador in self._observadores[:]:
                observador.actualizar(evento)

# ==============================================================================
# ARCHIVO 19/30: observer.py
# Directorio: patrones\observer
# Ruta completa: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\python_farma\patrones\observer\observer.py
# ==============================================================================

from typing import Generic, TypeVar, Any
from abc import ABC, abstractmethod

# Tipo genérico para el evento/dato que se notifica
T = TypeVar('T')

class Observer(Generic[T], ABC):
    """
    La interfaz Observer declara el método de actualización (actualizar), 
    utilizado por los Sujetos (Observables).
    """
    
    @abstractmethod
    def actualizar(self, evento: T) -> None:
        """
        Recibe la actualización desde el sujeto.
        
        Args:
            evento: El dato/evento notificado por el sujeto.
        """
        pass


################################################################################
# DIRECTORIO: patrones\registry
################################################################################

# ==============================================================================
# ARCHIVO 20/30: __init__.py
# Directorio: patrones\registry
# Ruta completa: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\python_farma\patrones\registry\__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 21/30: registros_servicios.py
# Directorio: patrones\registry
# Ruta completa: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\python_farma\patrones\registry\registros_servicios.py
# ==============================================================================

import threading
from typing import Any, Dict

class RegistroServicios:
    """
    Singleton que actúa como un registro central (Service Locator) 
    para los servicios clave de la aplicación (Logger, DBManager, etc.).
    
    Esta versión utiliza un flag __initialized para ser compatible con linters
    y seguir un patrón de inicialización más limpio.
    """
    _instance = None
    _lock = threading.Lock()
    _initialized = False  # Flag para controlar la inicialización

    def __new__(cls):
        """
        Controla la CREACIÓN de la instancia (Patrón Singleton).
        """
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    # Llama al __new__ de la clase base (object)
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """
        Controla la INICIALIZACIÓN de la instancia (Patrón Singleton).
        
        Esto se llama CADA VEZ que se intenta crear una instancia 
        (ej. RegistroServicios()), por eso usamos el flag '_initialized'.
        """
        if self._initialized:
            # Si ya está inicializado, no hacer nada.
            return
            
        # --- Lógica de inicialización (se ejecuta solo una vez) ---
        print("[Registry] Inicializando el registro de servicios por primera vez.")
        # ESTA es la línea que movimos aquí
        self._servicios: Dict[str, Any] = {}
        self._initialized = True  # Marcar como inicializado
        # ---------------------------------------------------------

    @classmethod
    def get_instance(cls):
        """
        Acceso a la instancia única.
        Llama a __new__ y __init__ implícitamente la primera vez.
        """
        # Si la instancia no existe, llamamos a cls()
        # Esto disparará __new__ (para crear) y luego __init__ (para inicializar)
        if cls._instance is None:
            cls() # Esto crea e inicializa la instancia
            
        return cls._instance

    def registrar_servicio(self, nombre: str, servicio: Any) -> None:
        """
        Registra una instancia de servicio bajo un nombre clave.
        """
        with self._lock:  # Es buena idea usar el lock al modificar el dict
            if nombre in self._servicios:
                print(f"[Registry] Advertencia: Sobrescribiendo servicio '{nombre}'.")
            self._servicios[nombre] = servicio
            print(f"[Registry] Servicio '{nombre}' registrado.")

    def get_servicio(self, nombre: str) -> Any:
        """
        Obtiene un servicio registrado por su nombre.
        """
        # La lectura de un diccionario es generalmente thread-safe en Python (GIL),
        # por lo que el lock no es estrictamente necesario aquí, pero self._servicios.get es atómico.
        servicio = self._servicios.get(nombre)
        if not servicio:
            raise ValueError(f"Servicio no registrado: {nombre}")
        return servicio


################################################################################
# DIRECTORIO: patrones\strategy
################################################################################

# ==============================================================================
# ARCHIVO 22/30: __init__.py
# Directorio: patrones\strategy
# Ruta completa: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\python_farma\patrones\strategy\__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 23/30: i_estrategia_descuento.py
# Directorio: patrones\strategy
# Ruta completa: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\python_farma\patrones\strategy\i_estrategia_descuento.py
# ==============================================================================

from abc import ABC, abstractmethod

class IEstrategiaDescuento(ABC):
    """
    Interfaz común para todas las estrategias de cálculo de descuento.
    """
    
    @abstractmethod
    def calcular_descuento(self, monto_total: float) -> float:
        """
        Calcula el descuento a aplicar sobre un monto total.
        
        Args:
            monto_total: El subtotal de la venta.
            
        Returns:
            El monto del descuento (no el precio final).
        """
        pass


################################################################################
# DIRECTORIO: patrones\strategy\implementacion
################################################################################

# ==============================================================================
# ARCHIVO 24/30: __init__.py
# Directorio: patrones\strategy\implementacion
# Ruta completa: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\python_farma\patrones\strategy\implementacion\__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 25/30: estrategias_descuento.py
# Directorio: patrones\strategy\implementacion
# Ruta completa: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\python_farma\patrones\strategy\implementacion\estrategias_descuento.py
# ==============================================================================

from python_farma.patrones.strategy.i_estrategia_descuento import IEstrategiaDescuento
from python_farma.constantes import (
    DTO_JUBILADO, DTO_OBRA_SOCIAL, DTO_SIN_DESCUENTO
)

class EstrategiaDescuentoJubilado(IEstrategiaDescuento):
    """Aplica el descuento configurado para jubilados."""
    def calcular_descuento(self, monto_total: float) -> float:
        descuento = monto_total * DTO_JUBILADO
        print(f"[Strategy] Aplicando EstrategiaDescuentoJubilado ({DTO_JUBILADO*100}%): ${descuento:.2f}")
        return descuento

class EstrategiaDescuentoObraSocial(IEstrategiaDescuento):
    """Aplica el descuento configurado para obras sociales."""
    def calcular_descuento(self, monto_total: float) -> float:
        descuento = monto_total * DTO_OBRA_SOCIAL
        print(f"[Strategy] Aplicando EstrategiaDescuentoObraSocial ({DTO_OBRA_SOCIAL*100}%): ${descuento:.2f}")
        return descuento

class EstrategiaSinDescuento(IEstrategiaDescuento):
    """Estrategia nula, no aplica ningún descuento."""
    def calcular_descuento(self, monto_total: float) -> float:
        print("[Strategy] Aplicando EstrategiaSinDescuento...")
        return monto_total * DTO_SIN_DESCUENTO


################################################################################
# DIRECTORIO: services
################################################################################

# ==============================================================================
# ARCHIVO 26/30: __init__.py
# Directorio: services
# Ruta completa: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\python_farma\services\__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 27/30: inventario_service.py
# Directorio: services
# Ruta completa: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\python_farma\services\inventario_service.py
# ==============================================================================

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

# ==============================================================================
# ARCHIVO 28/30: notificador_stock_bajo.py
# Directorio: services
# Ruta completa: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\python_farma\services\notificador_stock_bajo.py
# ==============================================================================

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

# ==============================================================================
# ARCHIVO 29/30: persistencia_service.py
# Directorio: services
# Ruta completa: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\python_farma\services\persistencia_service.py
# ==============================================================================

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

# ==============================================================================
# ARCHIVO 30/30: venta_service.py
# Directorio: services
# Ruta completa: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\python_farma\services\venta_service.py
# ==============================================================================

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


################################################################################
# FIN DEL INTEGRADOR FINAL
# Total de archivos: 30
# Generado: 2025-11-05 09:52:58
################################################################################
