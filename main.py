import time
from python_farma.config.configuracion import ConfiguracionSistema
from python_farma.patrones.registry.registros_servicios import RegistroServicios
from python_farma.services.inventario_service import InventarioService
from python_farma.services.notificador_stock_bajo import NotificadorStockBajo
from python_farma.services.venta_service import VentaService
from python_farma.patrones.strategy.implementacion.estrategias_descuento import (
    EstrategiaDescuentoJubilado,
    EstrategiaSinDescuento
)
from python_farma.excepciones.stock_insuficiente_excepcion import StockInsuficienteException

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
    # Obtenemos la instancia de configuración.
    # El mensaje "_cargar_configuracion" solo debe aparecer UNA VEZ.
    config = ConfiguracionSistema.get_instance()
    
    # --- Registry ---
    # Obtenemos la instancia del registro (que también es Singleton)
    registro = RegistroServicios.get_instance()
    
    # Registramos servicios
    registro.registrar_servicio("logger", LoggerServicio())
    # Usamos el Singleton 'config' para configurar otro servicio
    registro.registrar_servicio("db_manager", DBManager(config.get_db_host()))

    # Usamos un servicio del Registry
    logger = registro.get_servicio("logger")
    logger.info("Demostración de Singleton y Registry completada.")

    # Verificamos que Singleton es la misma instancia
    config2 = ConfiguracionSistema.get_instance()
    assert config is config2, "Error: Singleton falló, las instancias son diferentes."
    print("[OK] Singleton verificado (misma instancia).")


def demonstrate_factory_and_observer():
    """Demuestra Factory y Observer."""
    print("\n--- 2. DEMO FACTORY Y OBSERVER ---")
    
    # --- Configuración Observer ---
    # 1. Crear el Sujeto (Observable)
    inventario_service = InventarioService()
    
    # 2. Crear los Observadores
    email_compras = "compras@pythonfarma.com"
    notificador_compras = NotificadorStockBajo(email_destino=email_compras)
    
    # 3. Suscribir Observadores al Sujeto
    inventario_service.agregar_observador(notificador_compras)
    print("[Observer] 'NotificadorStockBajo' suscrito a 'InventarioService'.")

    # --- Factory ---
    # Usamos el servicio de inventario, que USA la Factory internamente.
    print("\n[Factory] Creando productos a través de InventarioService...")
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
    except ValueError as e:
        print(f"[Error] Falló la creación de producto: {e}")

    # --- Disparar Observer ---
    # Simulamos una venta que reduce el stock de Amoxicilina
    # Esto debería disparar la alerta del Notificador.
    print("\n[Observer] Simulando venta que dispara alerta de stock...")
    try:
        # El umbral es 10. Al descontar 3, el stock queda en 9.
        inventario_service.descontar_stock(
            nombre_producto="Amoxicilina 500mg", 
            cantidad=3
        )
    except StockInsuficienteException as e:
        print(f"[Error Venta] {e.mensaje}")

    return inventario_service # Retornamos para usar en la siguiente demo

def demonstrate_strategy(inventario: InventarioService):
    """Demuestra el Patrón Strategy."""
    print("\n--- 3. DEMO STRATEGY (PUNTO DE VENTA) ---")
    
    # --- Preparación ---
    # Creamos el Contexto (VentaService)
    venta_service = VentaService()
    
    # Obtenemos los productos del inventario
    try:
        perfume = inventario.get_producto("Perfume 'Olympea'")
        ibuprofeno = inventario.get_producto("Ibuprofeno 400mg")
        amoxicilina = inventario.get_producto("Amoxicilina 500mg")
    except ValueError as e:
        print(f"Error fatal: No se pudieron recuperar productos: {e}")
        return

    # --- Venta 1: Cliente Regular (Sin Descuento) ---
    print("\n[Strategy] PROCESANDO VENTA 1 (Cliente Regular)")
    carrito_1 = [perfume, ibuprofeno]
    # Usará la Estrategia por defecto (EstrategiaSinDescuento)
    venta_service.set_estrategia(EstrategiaSinDescuento())
    total_1 = venta_service.calcular_total_venta(carrito_1)
    
    # Simulamos la venta (descontar stock)
    try:
        inventario.descontar_stock("Perfume 'Olympea'", 1)
        inventario.descontar_stock("Ibuprofeno 400mg", 1)
    except StockInsuficienteException as e:
        print(f"[Error Venta] {e.mensaje}")

    # --- Venta 2: Cliente Jubilado (Con Descuento) ---
    print("\n[Strategy] PROCESANDO VENTA 2 (Cliente Jubilado)")
    carrito_2 = [amoxicilina]
    # Cambiamos la estrategia en tiempo de ejecución
    venta_service.set_estrategia(EstrategiaDescuentoJubilado())
    total_2 = venta_service.calcular_total_venta(carrito_2)

    # Simulamos la venta (descontar stock)
    try:
        inventario.descontar_stock("Amoxicilina 500mg", 1)
    except StockInsuficienteException as e:
        print(f"[Error Venta] {e.mensaje}")


def main():
    """Punto de entrada principal de la aplicación."""
    print("="*60)
    print("     SISTEMA DE GESTIÓN DE FARMACIA (PythonFarma)")
    print("     Demostración de Patrones de Diseño")
    print("="*60)
    
    # 1. Singleton y Registry
    demonstrate_singleton_and_registry()
    
    # 2. Factory y Observer
    # Esta función crea y retorna el inventario
    inventario_service = demonstrate_factory_and_observer()
    
    # 3. Strategy
    # Pasamos el inventario a la demo de estrategia
    demonstrate_strategy(inventario_service)
    
    print("\n" + "="*60)
    print("     DEMOSTRACIÓN FINALIZADA EXITOSAMENTE")
    print("="*60)
    print("Resumen de Patrones Aplicados:")
    print("[OK] SINGLETON: 'ConfiguracionSistema' cargada una sola vez.")
    print("[OK] REGISTRY: 'LoggerServicio' y 'DBManager' registrados y accedidos.")
    print("[OK] FACTORY: Productos creados sin exponer clases concretas.")
    print("[OK] OBSERVER: 'NotificadorStockBajo' recibió alerta de 'InventarioService'.")
    print("[OK] STRATEGY: 'VentaService' usó 'EstrategiaSinDescuento' y 'EstrategiaDescuentoJubilado'.")
    print("="*60)


if __name__ == "__main__":
    main()