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