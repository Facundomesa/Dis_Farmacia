# Sistema de Gestión de Farmacia (PythonFarma)

[![Python Version](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-PEP%208-orange.svg)](https://www.python.org/dev/peps/pep-0008/)

Sistema integral de gestión de farmacia que demuestra la implementación de patrones de diseño de software (Singleton, Factory, Observer, Strategy, Registry) con un enfoque educativo y profesional.

---

## Tabla de Contenidos

- [Contexto del Dominio](#contexto-del-dominio)
- [Caracteristicas Principales](#caracteristicas-principales)
- [Arquitectura del Sistema](#arquitectura-del-sistema)
- [Patrones de Diseno Implementados](#patrones-de-diseno-implementados)
- [Requisitos del Sistema](#requisitos-del-sistema)
- [Instalacion](#instalacion)
- [Uso del Sistema](#uso-del-sistema)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Modulos del Sistema](#modulos-del-sistema)
- [Documentacion Tecnica](#documentacion-tecnica)
- [Testing y Validacion](#testing-y-validacion)
- [Contribucion](#contribucion)
- [Licencia](#licencia)

---

## Contexto del Dominio

### Problema que Resuelve

El sistema **PythonFarmacia** aborda los desafíos de la gestión de una farmacia moderna, un dominio que requiere:

1.  **Gestión de Múltiples Tipos de Productos**
    * Productos con reglas de negocio distintas (Medicamentos con receta, Venta Libre/OTC, Perfumería).
    * Cada tipo con atributos y lógicas de descuento diferentes.

2.  **Monitoreo de Inventario en Tiempo Real**
    * Control de stock crítico para medicamentos.
    * Generación de alertas automáticas cuando el stock cae por debajo de un umbral mínimo.
    * Desacoplamiento entre el módulo de ventas y el de alertas.

3.  **Reglas de Negocio de Precios Complejas**
    * El precio final de una venta varía según múltiples factores (descuentos de obra social, promociones de jubilados, ofertas del día).
    * Necesidad de cambiar o agregar nuevas reglas de descuento sin modificar el código del Punto de Venta (POS).

4.  **Configuración Centralizada**
    * Datos críticos como la tasa de IVA, CUIT de la farmacia, y datos de conexión a BBDD deben ser consistentes en toda la aplicación.

5.  **Persistencia y Trazabilidad**
    * Almacenamiento de ventas, clientes y recetas para auditoría.

### Actores del Sistema

- **Administrador de Inventario**: Carga productos, define umbrales de stock.
- **Cajero**: Opera el Punto de Venta (POS), procesa ventas y aplica descuentos.
- **Gerente de Compras**: Recibe alertas de stock bajo para reponer mercadería.
- **Cliente**: Proporciona datos para descuentos (ej. credencial de obra social).

### Flujo de Operaciones Tipico

CONFIGURACION --> Se carga la instancia única de configuración (IVA, CUIT).

INICIO --> Se registran servicios (Logger, DB) en el Registry.

INVENTARIO --> Admin crea productos (Medicamentos, Perfumería) usando la Factory.

VENTA --> Cajero agrega productos al carrito.

DESCUENTO --> Sistema selecciona la Estrategia de Descuento (ej. Jubilado).

PROCESAR VENTA --> Se calcula el total y se reduce el stock del producto.

ALERTA (OBSERVER) --> Producto notifica cambio de stock. Observador (Notificador) detecta stock bajo y envía alerta al Gerente de Compras.


---

## Caracteristicas Principales

### Funcionalidades del Sistema

#### 1. Gestión de Productos (Patrón Factory)

- **Creación dinámica** de 3 tipos de productos mediante Factory Pattern:
    - **MedicamentoConReceta**: Requiere `receta_requerida=True`.
    - **MedicamentoOTC**: Venta libre (Over-The-Counter).
    - **Perfumeria**: Admite `descuento_promocion` adicional.
- El `InventarioService` utiliza la factory, desacoplando al cliente de las clases concretas.

#### 2. Sistema de Alertas de Stock (Patrón Observer)

- **Inventario Observable**: El `InventarioService` (o el `Producto`) actúa como **Sujeto** (Observable).
- **Notificadores Observadores**: Clases como `NotificadorStockBajo` actúan como **Observadores**.
- **Notificación Automática**: Al realizar una venta, el stock se reduce. Si cruza el umbral, el Sujeto `notifica_observadores()`.
- **Desacoplamiento**: El `VentaService` no sabe nada sobre el sistema de alertas. Solo descuenta stock.

#### 3. Punto de Venta con Descuentos (Patrón Strategy)

- **Algoritmos Intercambiables**: El `VentaService` (Contexto) calcula el total usando una estrategia de descuento.
- **Estrategias Concretas**:
    - `EstrategiaDescuentoJubilado`: Aplica un 40% (configurable).
    - `EstrategiaDescuentoObraSocial`: Aplica un 20% (configurable).
    - `EstrategiaSinDescuento`: Aplica 0%.
- **Extensibilidad**: Se pueden agregar nuevas promociones (ej. `EstrategiaPromoMartes`) sin modificar `VentaService`.

#### 4. Configuración Centralizada (Patrón Singleton)

- **Instancia Única**: `ConfiguracionSistema` es un Singleton.
- **Carga Única**: Lee el archivo `.env` o `config.ini` una sola vez al inicio.
- **Acceso Global**: Cualquier módulo (ej. `VentaService` para obtener IVA) accede a la misma instancia: `ConfiguracionSistema.get_instance().get_tasa_iva()`.

#### 5. Registro de Servicios (Patrón Registry)

- **Service Locator**: El `RegistroServicios` (implementado como Singleton) actúa como un "directorio" central.
- **Registro al Inicio**: En `main.py`, se registran servicios como `Logger` y `DBManager`.
- **Acceso Centralizado**: Cualquier otra clase obtiene dependencias llamando a `RegistroServicios.get_instance().get_servicio("logger")`.

---

## Arquitectura del Sistema

### Principios Arquitectonicos

El sistema esta disenado siguiendo principios SOLID:

- **Single Responsibility**:
    - `Entidades`: Solo contienen datos (DTOs).
    - `Servicios`: Solo contienen lógica de negocio.
    - `Patrones`: Implementaciones aisladas.

- **Open/Closed**:
    - Nuevos `Productos`: Se agregan a la `Factory` sin modificar el `InventarioService`.
    - Nuevos `Descuentos`: Se crea una nueva `Estrategia` sin modificar el `VentaService`.

- **Liskov Substitution**:
    - Todos los productos son `Producto`.
    - Todas las estrategias implementan `IEstrategiaDescuento`.

- **Interface Segregation**:
    - `Observer[T]` / `Observable[T]` son genéricos.
    - `IEstrategIAdescuento` es específica.

- **Dependency Inversion**:
    - `VentaService` depende de `IEstrategiaDescuento` (abstracción), no de `EstrategiaDescuentoJubilado` (concreta).
    - `InventarioService` depende de `Producto` (interfaz), no de `Perfumeria` (concreta).

### Separacion de Capas

+----------------------------------+ | PRESENTACION | | (main.py - Demostracion CLI) | +----------------------------------+ | v +----------------------------------+ | SERVICIOS DE DOMINIO | | (VentaService, InventarioService)| +----------------------------------+ | v +----------------------------------+ | ENTIDADES | | (Producto, Venta, Cliente) | +----------------------------------+ | v +----------------------------------+ | PATRONES / INFRAESTRUCTURA | | (Factory, Strategy, Observer, | | Config, Registry, Excepciones) | +----------------------------------+


### Inyeccion de Dependencias

El sistema utiliza inyección manual de dependencias, principalmente para el patrón Strategy.

```python
# Estrategia inyectada en constructor o setter
from python_farma.servicios.venta_service import VentaService
from python_farma.patrones.strategy.impl.estrategias_descuento import *

# Contexto (VentaService)
venta_service = VentaService()

# Inyectar estrategia para un cliente jubilado
cliente_es_jubilado = True
if cliente_es_jubilado:
    venta_service.set_estrategia(EstrategiaDescuentoJubilado())
else:
    venta_service.set_estrategia(EstrategiaSinDescuento())

# El servicio usa la estrategia inyectada
total = venta_service.calcular_total(carrito)
Patrones de Diseno Implementados
1. SINGLETON Pattern
Ubicacion: python_farma/config/configuracion.py

Problema que resuelve:

Garantizar una única instancia de ConfiguracionSistema.

Proveer un punto de acceso global a datos críticos (IVA, CUIT, BBDD).

Evitar leer el archivo config.ini o .env múltiples veces.

Implementacion:

Python

import threading

class ConfiguracionSistema:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        raise TypeError("Clase Singleton. Usar get_instance().")

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            with cls._lock:  # Thread-safe double-checked locking
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._cargar_configuracion()
        return cls._instance

    def _cargar_configuracion(self):
        # Lógica para leer .env o .ini
        self._tasa_iva = 0.21
        self._cuit = "30-12345678-9"
        print("[Singleton] Configuracion cargada desde archivo.")
Uso en el sistema:

VentaService lo usa para obtener el IVA.

DBManager lo usa para obtener credenciales de BBDD.

Ventajas:

Thread-safe.

Inicialización perezosa (lazy initialization).

Punto único de control.

2. FACTORY METHOD Pattern
Ubicacion: python_farma/patrones/factory/producto_factory.py

Problema que resuelve:

Encapsular la lógica de creación de diferentes tipos de Producto.

Desacoplar InventarioService de las clases concretas (MedicamentoConReceta, Perfumeria, etc.).

Facilitar la adición de nuevos tipos de productos.

Implementacion:

Python

from python_farma.entidades.producto import Producto
from python_farma.entidades.tipos_producto import *

class ProductoFactory:
    
    # Mapeo de tipos (string) a clases (constructor)
    _CREADORES = {
        "MedicamentoConReceta": MedicamentoConReceta,
        "MedicamentoOTC": MedicamentoOTC,
        "Perfumeria": Perfumeria
    }

    @staticmethod
    def crear_producto(tipo_producto: str, nombre: str, precio: float) -> Producto:
        
        creador = ProductoFactory._CREADORES.get(tipo_producto)
        
        if not creador:
            raise ValueError(f"Tipo de producto desconocido: {tipo_producto}")
            
        # Llama al constructor de la clase concreta (ej. Perfumeria(...))
        return creador(nombre=nombre, precio_base=precio)
Uso en el sistema:

Python

# InventarioService usa la factory
prod_a = inventario_service.crear_producto("Perfumeria", "Perfume", 5000)
prod_b = inventario_service.crear_producto("MedicamentoOTC", "Ibuprofeno", 700)
Ventajas:

Código cliente (InventarioService) independiente de clases concretas.

Fácil agregar nuevos productos.

Punto único de creación.

3. OBSERVER Pattern
Ubicacion: python_farma/patrones/observer/

Problema que resuelve:

Notificar a múltiples objetos (Observadores) sobre un cambio de estado en otro objeto (Sujeto).

Desacoplar el InventarioService (que cambia el stock) del NotificadorStockBajo (que envía alertas).

Implementacion:

Python

# Interfaces genéricas (Tipo-seguras)
from typing import Generic, TypeVar, List
from abc import ABC, abstractmethod

T = TypeVar('T')

class Observer(Generic[T], ABC):
    @abstractmethod
    def actualizar(self, evento: T) -> None:
        pass

class Observable(Generic[T], ABC):
    def __init__(self):
        self._observadores: List[Observer[T]] = []

    def agregar_observador(self, observador: Observer[T]) -> None:
        self._observadores.append(observador)

    def notificar_observadores(self, evento: T) -> None:
        for observador in self._observadores:
            observador.actualizar(evento)
Uso en el sistema:

Python

# Sujeto/Observable (Notifica el nuevo stock: int)
class InventarioService(Observable[int]):
    def descontar_stock(self, producto: Producto, cantidad: int):
        # ...lógica para descontar...
        if producto.stock < producto.umbral_minimo:
            # Notifica a todos los observadores el nuevo stock
            self.notificar_observadores(producto.stock)

# Observador
class NotificadorStockBajo(Observer[int]):
    def actualizar(self, nuevo_stock: int) -> None:
        # Reacciona al evento
        print(f"[Observer] ALERTA: Stock bajo detectado: {nuevo_stock} unidades.")
        # ...enviar email...
Ventajas:

Desacoplamiento total entre Sujeto y Observadores.

Tipo-seguro con Generics.

Permite múltiples observadores (ej. NotificadorStockBajo, ActualizadorDashboard).

4. STRATEGY Pattern

Getty Images

Ubicacion: python_farma/patrones/strategy/

Problema que resuelve:

Permitir que un algoritmo (cálculo de descuento) sea intercambiable en tiempo de ejecución.

Evitar una cascada de if/elif/else en el VentaService.

Facilitar la adición de nuevas reglas de descuento.

Implementacion:

Python

from abc import ABC, abstractmethod

# Interfaz
class IEstrategiaDescuento(ABC):
    @abstractabstractmethod
    def calcular_descuento(self, monto_total: float) -> float:
        pass

# Estrategia 1
class EstrategiaDescuentoJubilado(IEstrategiaDescuento):
    def calcular_descuento(self, monto_total: float) -> float:
        return monto_total * 0.40 # 40% Dto

# Estrategia 2
class EstrategiaDescuentoObraSocial(IEstrategiaDescuento):
    def calcular_descuento(self, monto_total: float) -> float:
        return monto_total * 0.20 # 20% Dto

# Estrategia 3
class EstrategiaSinDescuento(IEstrategiaDescuento):
    def calcular_descuento(self, monto_total: float) -> float:
        return 0.0
Uso en el sistema:

Python

# Contexto
class VentaService:
    def __init__(self, estrategia: IEstrategiaDescuento = EstrategiaSinDescuento()):
        self._estrategia = estrategia
        
    def set_estrategia(self, estrategia: IEstrategiaDescuento):
        self._estrategia = estrategia

    def calcular_total_venta(self, subtotal: float) -> float:
        # Delega el cálculo a la estrategia actual
        descuento = self._estrategia.calcular_descuento(subtotal)
        return subtotal - descuento
Ventajas:

Algoritmos intercambiables.

Oculta la complejidad de las reglas de negocio al cliente (VentaService).

Fácil de testear cada estrategia por separado.

5. REGISTRY Pattern (Bonus)
Ubicacion: python_farma/patrones/registry/registro_servicios.py

Problema que resuelve:

Proveer un "directorio" centralizado (Service Locator) para servicios comunes.

Reducir el acoplamiento evitando imports directos de servicios en clases de bajo nivel.

Evitar pasar dependencias (como Logger) a través de múltiples capas.

Implementacion:

Python

import threading

class RegistroServicios:
    # Implementado como un Singleton
    _instance = None
    _lock = threading.Lock()
    
    @classmethod
    def get_instance(cls):
        # ... (código de Singleton) ...
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._servicios = {} # Inicializa el registro
        return cls._instance

    def registrar_servicio(self, nombre: str, servicio: object) -> None:
        self._servicios[nombre] = servicio
        print(f"[Registry] Servicio '{nombre}' registrado.")

    def get_servicio(self, nombre: str) -> object:
        servicio = self._servicios.get(nombre)
        if not servicio:
            raise ValueError(f"Servicio no registrado: {nombre}")
        return servicio
Uso en el sistema:

Python

# En main.py (al inicio)
registro = RegistroServicios.get_instance()
registro.registrar_servicio("logger", LoggerServicio())
registro.registrar_servicio("db_manager", GestorConexionDB())

# En cualquier otra clase del sistema
logger = RegistroServicios.get_instance().get_servicio("logger")
logger.info("El sistema ha iniciado.")
Ventajas:

Desacopla al consumidor del proveedor del servicio.

Punto único de gestión de servicios.

Requisitos del Sistema
Requisitos de Software
Python 3.13 o superior

Sistema Operativo: Windows, Linux, macOS

Modulos Estandar: Solo biblioteca estandar de Python (sin dependencias externas)

Requisitos de Hardware
RAM: Minimo 512 MB

Disco: 50 MB libres

Instalacion
1. Clonar el Repositorio
Bash

git clone [https://github.com/usuario/python-farma.git](https://github.com/usuario/python-farma.git)
cd python-farma
2. Crear Entorno Virtual
Windows:
Bash

python -m venv .venv
.venv\Scripts\activate
Linux/macOS:
Bash

python3 -m venv .venv
source .venv/bin/activate
3. Verificar Instalacion
Bash

python --version
# Debe mostrar Python 3.13 o superior
4. Ejecutar Sistema
Bash

python main.py
Salida esperada:

======================================================================
         SISTEMA DE GESTION DE FARMACIA - PATRONES DE DISENO
======================================================================

[Singleton] Configuracion cargada desde archivo.
[Registry] Servicio 'logger' registrado.
[Registry] Servicio 'db_manager' registrado.

----------------------------------------------------------------------
  PATRON FACTORY: Creando productos...
----------------------------------------------------------------------
[Factory] Creado producto: Perfume 'Olympea' (Perfumeria)
[Factory] Creado producto: Amoxicilina 500mg (MedicamentoConReceta)

----------------------------------------------------------------------
  PATRON STRATEGY: Procesando ventas...
----------------------------------------------------------------------
[Venta] Subtotal: 5000.00
[Strategy] Aplicando EstrategiaSinDescuento...
[Venta] TOTAL VENTA 1: 5000.00

[Venta] Subtotal: 1500.00
[Strategy] Aplicando EstrategiaDescuentoJubilado (40%)...
[Venta] TOTAL VENTA 2: 900.00

----------------------------------------------------------------------
  PATRON OBSERVER: Simulando stock bajo...
----------------------------------------------------------------------
[Venta] Descontando stock de 'Amoxicilina 500mg'. Stock actual: 9
[Observer] ALERTA: Stock bajo detectado: 9 unidades. (Email enviado a compras@farma.com)

======================================================================
               EJEMPLO COMPLETADO EXITOSAMENTE
======================================================================
  [OK] SINGLETON - ConfiguracionSistema (instancia unica)
  [OK] FACTORY   - Creacion de 3 tipos de productos
  [OK] OBSERVER  - Alerta de stock bajo
  [OK] STRATEGY  - Calculo de descuentos (Jubilado y Normal)
  [OK] REGISTRY  - Acceso a servicio 'logger'
======================================================================
Uso del Sistema
Ejemplo Básico (main.py)
Python

# 1. Obtener configuración (SINGLETON)
config = ConfiguracionSistema.get_instance()
tasa_iva = config.get_tasa_iva()

# 2. Registrar servicios (REGISTRY)
registro = RegistroServicios.get_instance()
registro.registrar_servicio("logger", LoggerServicio())

# 3. Crear productos (FACTORY)
inv_service = InventarioService()
prod_perfume = inv_service.crear_producto("Perfumeria", "Perfume", 5000)
prod_med = inv_service.crear_producto("MedicamentoConReceta", "Amoxicilina", 1500)

# 4. Configurar Alertas (OBSERVER)
notificador = NotificadorStockBajo(email_destino="compras@farma.com")
inv_service.agregar_observador(notificador) # Suscripción

# 5. Procesar Venta (STRATEGY)
venta_service = VentaService() # Usa estrategia por defecto (SinDescuento)
total_1 = venta_service.calcular_total_venta(prod_perfume.precio)

# Cambiar estrategia
venta_service.set_estrategia(EstrategiaDescuentoJubilado())
total_2 = venta_service.calcular_total_venta(prod_med.precio)

# 6. Descontar stock (Dispara OBSERVER)
inv_service.descontar_stock(prod_med, 1)
Persistencia de Datos (Ejemplo con Pickle)
Python

import pickle
from python_farma.entidades.cliente import Cliente

cliente = Cliente(dni="123456", nombre="Juan Perez", es_jubilado=True)

# Persistir
with open("data/cliente_123456.dat", "wb") as f:
    pickle.dump(cliente, f)

# Recuperar
with open("data/cliente_123456.dat", "rb") as f:
    cliente_recuperado = pickle.load(f)
    
print(f"Cliente recuperado: {cliente_recuperado.get_nombre()}")
Estructura del Proyecto
PythonFarma/
|
+-- main.py                       # Punto de entrada y demo de integración
+-- README.md                     # Este archivo
+-- historiasdeusuario.md         # Historias de Usuario (US)
|
+-- .venv/                        # Entorno virtual Python
|
+-- data/                         # Datos persistidos (ej. .dat)
|
+-- python_farma/                 # Paquete principal
    |
    +-- __init__.py
    +-- constantes.py             # Constantes (IVA_JUBILADO, UMBRAL_STOCK)
    |
    +-- entidades/                # Objetos de dominio (DTOs)
    |   +-- __init__.py
    |   +-- producto.py           # Interfaz base Producto
    |   +-- tipos_producto.py     # Clases concretas: Medicamento, Perfumeria, etc.
    |   +-- cliente.py
    |   +-- venta.py
    |   +-- receta.py
    |
    +-- servicios/                # Lógica de negocio
    |   +-- __init__.py
    |   +-- inventario_service.py # (Sujeto/Observable)
    |   +-- venta_service.py      # (Contexto de Strategy)
    |   +-- notificador_stock_bajo.py # (Observador)
    |
    +-- config/
    |   +-- __init__.py
    |   +-- configuracion.py      # (Implementación de Singleton)
    |
    +-- patrones/                 # Definiciones de patrones
    |   +-- __init__.py
    |   |
    |   +-- factory/
    |   |   +-- __init__.py
    |   |   +-- producto_factory.py # (Implementación de Factory)
    |   |
    |   +-- observer/
    |   |   +-- __init__.py
    |   |   +-- observable.py     # Interfaz Observable[T]
    |   |   +-- observer.py       # Interfaz Observer[T]
    |   |
    |   +-- strategy/
    |   |   +-- __init__.py
    |   |   +-- i_estrategia_descuento.py # Interfaz Strategy
    |   |   +-- impl/
    |   |       +-- __init__.py
    |   |       +-- estrategias_descuento.py # Implementaciones concretas
    |   |
    |   +-- registry/
    |       +-- __init__.py
    |       +-- registro_servicios.py # (Implementación de Registry)
    |
    +-- excepciones/              # Excepciones personalizadas
        +-- __init__.py
        +-- farmacia_exception.py
        +-- stock_insuficiente_exception.py
Modulos del Sistema
Modulo: entidades
Responsabilidad: Objetos de dominio puros (DTOs).

Producto: Interfaz base.

tipos_producto.py: Contiene MedicamentoConReceta, MedicamentoOTC, Perfumeria.

Venta, Cliente: Almacenan datos de transacciones y usuarios.

Modulo: servicios
Responsabilidad: Lógica de negocio (Orquestadores).

InventarioService: Maneja el stock. Actúa como Sujeto Observable.

VentaService: Procesa ventas. Actúa como Contexto de Strategy.

NotificadorStockBajo: Envía alertas. Actúa como Observador.

Modulo: patrones
Responsabilidad: Implementaciones genéricas y concretas de los patrones.

factory/producto_factory.py: Implementación de Factory Method.

strategy/i_estrategia_descuento.py: Interfaz de Strategy.

observer/observable.py: Interfaz de Observer.

registry/registro_servicios.py: Implementación de Registry.

Modulo: config
Responsabilidad: Configuración global.

configuracion.py: Implementación de Singleton.

Modulo: excepciones
Responsabilidad: Errores de dominio específicos.

StockInsuficienteException: Lanzada por InventarioService si la venta no puede completarse.

Documentacion Tecnica
Convenciones de Codigo
PEP 8 Compliance (100%)
Nombres de variables: snake_case

Nombres de clases: PascalCase

Constantes: UPPER_SNAKE_CASE en constantes.py

Privados: Prefijo _nombre

Docstrings (Google Style)
Python

def mi_metodo(self, parametro: str) -> bool:
    """
    Descripcion breve del metodo.

    Args:
        parametro: Descripcion del parametro.

    Returns:
        Descripcion del valor de retorno.

    Raises:
        ValueError: Si el parametro es invalido.
    """
Type Hints
Se utiliza typing extensivamente para claridad y validación estática.

Python

from typing import List, Optional

def procesar_clientes(self, clientes: List[Cliente]) -> Optional[Cliente]:
    pass
Configuracion de Constantes
Todas las constantes en constantes.py:

Python

# Descuentos
DTO_JUBILADO = 0.40  # 40%
DTO_OBRA_SOCIAL = 0.20 # 20%

# Stock
UMBRAL_MINIMO_STOCK_MEDICAMENTOS = 10

# Impuestos
TASA_IVA_GENERAL = 0.21
Testing y Validacion
Ejecucion del Sistema Completo
El archivo main.py actúa como un script de prueba de integración que valida el flujo completo y la correcta implementación de todos los patrones.

[x] Patron Singleton - Instancia única de configuración.

[x] Patron Registry - Registro y obtención de servicios.

[x] Patron Factory - Creación de 3 tipos de productos.

[x] Patron Strategy - Cálculo de descuentos (Jubilado vs SinDescuento).

[x] Patron Observer - Notificación de stock bajo.

[x] Manejo de Excepciones (simulado).

Casos de Prueba
Caso 1: Stock Insuficiente
Python

try:
    inventario_service.descontar_stock(producto, 100) # Stock disponible: 50
except StockInsuficienteException as e:
    assert e.get_stock_requerido() == 100
    assert e.get_stock_disponible() == 50
Caso 2: Cálculo con Strategy
Python

venta_service = VentaService()
subtotal = 100.0

# Test Estrategia 1
venta_service.set_estrategia(EstrategiaSinDescuento())
assert venta_service.calcular_total_venta(subtotal) == 100.0

# Test Estrategia 2
venta_service.set_estrategia(EstrategiaDescuentoJubilado())
assert venta_service.calcular_total_venta(subtotal) == 60.0 # 100 * (1 - 0.40)
Caso 3: Singleton Único
Python

config1 = ConfiguracionSistema.get_instance()
config2 = ConfiguracionSistema.get_instance()

assert config1 is config2 # Deben ser el mismo objeto en memoria
Contribucion
Como Agregar un Nuevo Tipo de Producto
Paso 1: Definir Entidad
En entidades/tipos_producto.py, agregar la nueva clase:

Python

from python_farma.entidades.producto import Producto

# ... (otras clases) ...

class SuplementoDietario(Producto):
    """Entidad Suplemento - solo datos."""
    def __init__(self, nombre: str, precio_base: float):
        super().__init__(nombre, precio_base)
        # Atributos específicos si los tuviera
        self._requiere_consulta = True

    def get_tipo_producto(self) -> str:
        return "SuplementoDietario"
Paso 2: Registrar en Factory
En patrones/factory/producto_factory.py:

Python

from python_farma.entidades.tipos_producto import *

class ProductoFactory:
    
    _CREADORES = {
        "MedicamentoConReceta": MedicamentoConReceta,
        "MedicamentoOTC": MedicamentoOTC,
        "Perfumeria": Perfumeria,
        "SuplementoDietario": SuplementoDietario  # <-- AGREGAR AQUI
    }

    # ... (el resto del método crear_producto no cambia) ...
Paso 3: Usar el Nuevo Producto
Python

# En main.py o donde sea necesario
nuevo_suplemento = inventario_service.crear_producto(
    "SuplementoDietario", 
    "Proteina Whey", 
    12000.0
)
Licencia
Este proyecto es de código abierto y esta disponible bajo la licencia MIT.

Ultima actualizacion: Noviembre 2025 Version del sistema: 1.0.0 Python requerido: 3.13+