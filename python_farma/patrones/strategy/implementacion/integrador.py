"""
Archivo integrador generado automaticamente
Directorio: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\python_farma\patrones\strategy\implementacion
Fecha: 2025-11-05 10:11:11
Total de archivos integrados: 2
"""

# ================================================================================
# ARCHIVO 1/2: __init__.py
# Ruta: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\python_farma\patrones\strategy\implementacion\__init__.py
# ================================================================================



# ================================================================================
# ARCHIVO 2/2: estrategias_descuento.py
# Ruta: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\python_farma\patrones\strategy\implementacion\estrategias_descuento.py
# ================================================================================

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

