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