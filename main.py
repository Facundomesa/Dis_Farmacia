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