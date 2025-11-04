# Historias de Usuario - Sistema de Gestión de Farmacia

**Proyecto**: PythonFarma
**Version**: 1.0.0
**Fecha**: Noviembre 2025
**Metodologia**: User Story Mapping

---

## Indice

1. [Epic 1: Gestión de Configuración y Servicios](#epic-1-gestión-de-configuración-y-servicios)
2. [Epic 2: Gestión de Inventario y Productos](#epic-2-gestión-de-inventario-y-productos)
3. [Epic 3: Punto de Venta (POS)](#epic-3-punto-de-venta-pos)
4. [Epic 4: Sistema de Alertas de Stock](#epic-4-sistema-de-alertas-de-stock)
5. [Historias Tecnicas (Patrones de Diseno)](#historias-tecnicas-patrones-de-diseno)

---

## Epic 1: Gestión de Configuración y Servicios

### US-001: Cargar Configuración Única del Sistema

**Como** administrador del sistema
**Quiero** que los datos críticos (IVA, CUIT, datos de DB) se carguen una sola vez
**Para** asegurar que todos los módulos usen valores consistentes

#### Criterios de Aceptacion

- [x] El sistema debe cargar un archivo `.env` o `config.ini` al arrancar.
- [x] Debe haber una única instancia global de `ConfiguracionSistema`.
- [x] Cualquier módulo (Ventas, Inventario) debe poder acceder a la misma instancia.
- [x] Implementar usando el patrón **Singleton**.

#### Detalles Tecnicos

**Clase**: `ConfiguracionSistema` (`python_farma/config/configuracion.py`)
**Patrón**: Singleton (ver US-TECH-001)

**Codigo de ejemplo**:
```python
from python_farma.config.configuracion import ConfiguracionSistema

# Obtener la instancia única (se crea la primera vez)
config = ConfiguracionSistema.get_instance()

# Usar los valores en cualquier parte
tasa_iva = config.get_tasa_iva() # ej: 0.21
cuit = config.get_cuit() # ej: 30-12345678-9
Trazabilidad: main.py linea 15, venta_service.py linea 40

US-002: Registrar Servicios Centrales de la Aplicación
Como desarrollador Quiero un registro central para acceder a servicios comunes (Logger, DBManager) Para evitar la importación global o el paso de dependencias por múltiples capas

Criterios de Aceptacion
[x] El sistema debe tener un RegistroServicios (que será un Singleton).

[x] Al inicio, se deben "registrar" servicios clave como Logger y DBManager.

[x] Cualquier clase debe poder solicitar un servicio por su nombre (string).

[x] Implementar usando el patrón Registry.

Detalles Tecnicos
Clase: RegistroServicios (python_farma/patrones/registry/registro_servicios.py) Patrón: Registry (ver US-TECH-005)

Codigo de ejemplo:

Python

from python_farma.patrones.registry.registro_servicios import RegistroServicios

# En main.py (al inicio)
registro = RegistroServicios.get_instance()
registro.registrar_servicio("logger", LoggerServicio())
registro.registrar_servicio("db_manager", GestorConexionDB())

# En cualquier otra clase
logger = RegistroServicios.get_instance().get_servicio("logger")
logger.info("Sistema iniciado.")
Trazabilidad: main.py lineas 20-25, producto_service.py linea 18

Epic 2: Gestión de Inventario y Productos
US-003: Crear Nuevos Productos en Inventario
Como administrador de inventario Quiero crear diferentes tipos de productos (Medicamento, Perfumería, Venta Libre) Para que el sistema maneje sus propiedades y reglas específicas

Criterios de Aceptacion
[x] El sistema debe soportar 3 tipos de productos:

MedicamentoConReceta (requiere receta_requerida=True)

MedicamentoOTC (Venta Libre)

Perfumeria (tiene descuento_promocion)

[x] La creación debe realizarse a través de una fábrica.

[x] El administrador no debe instanciar las clases concretas directamente.

[x] Implementar usando el patrón Factory Method.

Detalles Tecnicos
Clase: ProductoFactory (python_farma/patrones/factory/producto_factory.py) Servicio: InventarioService Entidades: MedicamentoConReceta, MedicamentoOTC, Perfumeria Patrón: Factory Method (ver US-TECH-002)

Codigo de ejemplo:

Python

from python_farma.servicios.inventario_service import InventarioService

inv_service = InventarioService()

# La factory se usa dentro del servicio
producto_a = inv_service.crear_producto(
    tipo_producto="MedicamentoConReceta",
    nombre="Amoxicilina 500mg",
    precio_base=1500.0
)

producto_b = inv_service.crear_producto(
    tipo_producto="Perfumeria",
    nombre="Perfume 'Olympea'",
    precio_base=35000.0
)
Validaciones:

Python

# Lanzar ValueError si el tipo no existe
inv_service.crear_producto(tipo_producto="Juguete", ...) # ValueError: Tipo de producto desconocido
Trazabilidad: main.py lineas 50-60

US-004: Descontar Stock al Realizar Venta
Como sistema de ventas Quiero descontar el stock de un producto cuando se vende Para mantener el inventario actualizado

Criterios de Aceptacion
[x] Al procesar una Venta, el InventarioService debe ser llamado.

[x] El método descontar_stock(producto, cantidad) debe:

Reducir la cantidad de producto.stock.

Verificar si el stock cae por debajo del umbral_minimo.

Si cae por debajo, debe notificar a los observadores.

[x] Implementar usando el patrón Observer (el producto es el Sujeto/Observable).

Detalles Tecnicos
Servicio: InventarioService.descontar_stock() Patrón: Observer (ver US-TECH-003)

Codigo de ejemplo:

Python

# El servicio de Ventas llama a esto
try:
    # Esto notificará automáticamente al NotificadorStockBajo
    inventario_service.descontar_stock(producto="Amoxicilina 500mg", cantidad=5)
except StockInsuficienteException as e:
    print(f"Error: No hay stock suficiente de {e.producto}")
Trazabilidad: venta_service.py linea 110, inventario_service.py lineas 80-105

Epic 3: Punto de Venta (POS)
US-005: Aplicar Descuentos Específicos a una Venta
Como cajero Quiero aplicar diferentes tipos de descuentos (Jubilado, Obra Social, Promoción) Para calcular el precio final correcto para el cliente

Criterios de Aceptacion
[x] El sistema debe poder calcular el total de una venta aplicando una regla de descuento.

[x] Deben existir al menos 3 estrategias de descuento:

EstrategiaDescuentoJubilado (ej. 40% dto)

EstrategiaDescuentoObraSocial (ej. 20% dto)

EstrategiaSinDescuento (0% dto)

[x] El módulo de Venta no debe contener if/elif/else para los tipos de descuento.

[x] Implementar usando el patrón Strategy.

Detalles Tecnicos
Clase: VentaService (Contexto) Interfaz: IEstrategiaDescuento (python_farma/patrones/strategy/i_estrategia_descuento.py) Estrategias: EstrategiaDescuentoJubilado, EstrategiaDescuentoObraSocial Patrón: Strategy (ver US-TECH-004)

Codigo de ejemplo:

Python

from python_farma.servicios.venta_service import VentaService
from python_farma.patrones.strategy.estrategias_descuento import *

# El cliente es Jubilado
cliente = cliente_service.get_cliente(dni="123456")
estrategia_jubilado = EstrategiaDescuentoJubilado()

venta_service = VentaService(estrategia_descuento=estrategia_jubilado)
total = venta_service.calcular_total(carrito) # Aplica 40% dto

# El cliente paga con Obra Social
estrategia_os = EstrategiaDescuentoObraSocial(convenio="OSDE")
venta_service.set_estrategia(estrategia_os)
total = venta_service.calcular_total(carrito) # Aplica 20% dto
Trazabilidad: main.py lineas 70-85, venta_service.py lineas 30-55

Epic 4: Sistema de Alertas de Stock
US-006: Definir Producto como Sujeto Observable
Como arquitecto de software Quiero que la entidad Producto pueda ser "observada" Para que otros módulos puedan reaccionar a sus cambios de estado (ej. cambio de stock)

Criterios de Aceptacion
[x] La clase Producto (o un GestorInventario) debe implementar la interfaz Observable.

[x] Debe permitir agregar_observador() y eliminar_observador().

[x] Debe tener un método notificar_observadores(evento) que se llama cuando el stock cambia.

[x] Implementar usando el patrón Observer.

Detalles Tecnicos
Clase: Producto (o GestorInventario) (python_farma/entidades/producto.py) Interfaz: Observable (python_farma/patrones/observer/observable.py) Patrón: Observer (ver US-TECH-003)

Codigo de ejemplo:

Python

class Producto(Observable[int]): # Notifica el nuevo stock (int)
    
    def set_stock(self, nuevo_stock: int):
        self._stock = nuevo_stock
        
        # Notificar a todos los suscriptores
        self.notificar_observadores(self._stock)
Trazabilidad: producto.py lineas 10-40, inventario_service.py linea 95

US-007: Generar Alerta de Email por Stock Bajo
Como gerente de compras Quiero recibir una notificación por email cuando un producto tenga stock bajo Para poder realizar un pedido de reposición a tiempo

Criterios de Aceptacion
[x] Debe existir una clase NotificadorStockBajo que implemente la interfaz Observer.

[x] Esta clase debe "suscribirse" al GestorInventario (o a los productos).

[x] Cuando reciba una notificación (método actualizar()), debe:

Comprobar si nuevo_stock < umbral_minimo.

Si es así, simular el envío de un email.

[x] Implementar usando el patrón Observer.

Detalles Tecnicos
Clase: NotificadorStockBajo (python_farma/servicios/notificador_stock_bajo.py) Interfaz: Observer (python_farma/patrones/observer/observer.py) Patrón: Observer (ver US-TECH-003)

Codigo de ejemplo:

Python

# En main.py (al inicio)
from python_farma.servicios.notificador_stock_bajo import NotificadorStockBajo
from python_farma.servicios.inventario_service import InventarioService

# Crear el observador
notificador_compras = NotificadorStockBajo(email_destino="compras@farma.com")

# Crear el sujeto (Observable)
inventario_service = InventarioService()

# Suscripción
inventario_service.agregar_observador_stock(notificador_compras)

# ... más tarde, cuando se llama a inventario_service.descontar_stock() ...
Salida esperada (en consola):

Enviando email a compras@farma.com:
Asunto: ALERTA DE STOCK BAJO
Mensaje: El producto 'Amoxicilina 500mg' ha alcanzado 9 unidades.
Trazabilidad: main.py lineas 30-35, notificador_stock_bajo.py lineas 15-50

Historias Tecnicas (Patrones de Diseno)
US-TECH-001: Implementar Singleton para ConfiguracionSistema
Como arquitecto de software Quiero garantizar una única instancia de ConfiguracionSistema Para asegurar estado global consistente y evitar lecturas repetidas de disco

Criterios de Aceptacion
[x] Implementar patrón Singleton thread-safe.

[x] Usar double-checked locking con threading.Lock.

[x] Constructor __new__ controla la instanciación.

[x] Método estático get_instance() para acceso global.

[x] La carga del archivo .env debe ocurrir solo una vez.

Detalles Tecnicos
Clase: ConfiguracionSistema Patrón: Singleton

Implementacion:

Python

import threading

class ConfiguracionSistema:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        raise TypeError("Usar get_instance() para obtener la instancia")

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            with cls._lock:  # Thread-safe
                if cls._instance is None:  # Double-checked
                    # Creamos la instancia real
                    cls._instance = super().__new__(cls)
                    # Inicializamos (cargamos el .env)
                    cls._instance._cargar_configuracion()
        return cls._instance

    def _cargar_configuracion(self):
        # Logica para leer .env (ej. con python-dotenv)
        self._tasa_iva = 0.21 # Valor cargado
        self._cuit = "30-12345678-9" # Valor cargado
        print("Configuracion cargada desde archivo.")

    def get_tasa_iva(self) -> float:
        return self._tasa_iva
Trazabilidad: python_farma/config/configuracion.py

US-TECH-002: Implementar Factory Method para Creacion de Productos
Como arquitecto de software Quiero centralizar la creación de tipos de Producto Para desacoplar el InventarioService de las clases concretas de productos

Criterios de Aceptacion
[x] Crear clase ProductoFactory con método estático crear_producto.

[x] Soportar creación de: MedicamentoConReceta, MedicamentoOTC, Perfumeria.

[x] Usar un diccionario de métodos de creación (no if/elif cascades).

[x] Lanzar ValueError si el tipo de producto es desconocido.

[x] Retornar la interfaz base Producto.

Detalles Tecnicos
Clase: ProductoFactory Patrón: Factory Method

Implementacion:

Python

from python_farma.entidades.producto import Producto
from python_farma.entidades.tipos_producto import *

class ProductoFactory:
    
    _CREADORES = {
        "MedicamentoConReceta": MedicamentoConReceta,
        "MedicamentoOTC": MedicamentoOTC,
        "Perfumeria": Perfumeria
    }

    @staticmethod
    def crear_producto(tipo_producto: str, nombre: str, precio_base: float) -> Producto:
        
        creador = ProductoFactory._CREADORES.get(tipo_producto)
        
        if not creador:
            raise ValueError(f"Tipo de producto desconocido: {tipo_producto}")
            
        # Llama al constructor de la clase concreta (ej. Perfumeria)
        return creador(nombre=nombre, precio_base=precio_base)
Trazabilidad: python_farma/patrones/factory/producto_factory.py

US-TECH-003: Implementar Observer Pattern Genérico
Como arquitecto de software Quiero implementar las interfaces Observer y Observable con Generics Para notificar cambios de estado de forma tipo-segura

Criterios de Aceptacion
[x] Crear clase abstracta Observable[T] genérica.

[x] Crear interfaz abstracta Observer[T] genérica.

[x] Observable debe manejar una lista de Observer (thread-safe).

[x] Métodos: agregar_observador(), notificar_observadores(evento: T).

[x] Observer debe tener actualizar(evento: T).

Detalles Tecnicos
Clases: Observable[T], Observer[T] Patrón: Observer

Implementacion:

Python

from typing import Generic, TypeVar, List
from abc import ABC, abstractmethod
import threading

T = TypeVar('T')

class Observer(Generic[T], ABC):
    @abstractmethod
    def actualizar(self, evento: T) -> None:
        pass

class Observable(Generic[T], ABC):
    def __init__(self):
        self._observadores: List[Observer[T]] = []
        self._lock = threading.Lock()

    def agregar_observador(self, observador: Observer[T]) -> None:
        with self._lock:
            if observador not in self._observadores:
                self._observadores.append(observador)

    def notificar_observadores(self, evento: T) -> None:
        with self._lock:
            for observador in self._observadores:
                observador.actualizar(evento)
Trazabilidad: python_farma/patrones/observer/observable.py, observer.py

US-TECH-004: Implementar Strategy Pattern para Descuentos
Como arquitecto de software Quiero algoritmos intercambiables para calcular descuentos Para permitir agregar nuevas reglas de negocio (descuentos) sin modificar el VentaService

Criterios de Aceptacion
[x] Crear interfaz IEstrategiaDescuento abstracta (método calcular_descuento).

[x] Implementar EstrategiaDescuentoJubilado (aplica 40%).

[x] Implementar EstrategiaDescuentoObraSocial (aplica 20%).

[x] Implementar EstrategiaSinDescuento (aplica 0%).

[x] El VentaService (Contexto) recibe una estrategia por inyección de dependencias.

Detalles Tecnicos
Interfaz: IEstrategiaDescuento Implementaciones: EstrategiaDescuentoJubilado, EstrategiaDescuentoObraSocial Patrón: Strategy

Implementacion:

Python

from abc import ABC, abstractmethod

class IEstrategiaDescuento(ABC):
    @abstractmethod
    def calcular_descuento(self, monto_total: float) -> float:
        pass

class EstrategiaDescuentoJubilado(IEstrategiaDescuento):
    def calcular_descuento(self, monto_total: float) -> float:
        return monto_total * 0.40 # 40% Dto

class EstrategiaDescuentoObraSocial(IEstrategiaDescuento):
    def calcular_descuento(self, monto_total: float) -> float:
        return monto_total * 0.20 # 20% Dto

# Contexto (VentaService)
class VentaService:
    def __init__(self, estrategia_descuento: IEstrategiaDescuento):
        self._estrategia = estrategia_descuento
        
    def set_estrategia(self, estrategia: IEstrategiaDescuento):
        self._estrategia = estrategia

    def calcular_total(self, carrito) -> float:
        subtotal = sum(item.precio for item in carrito)
        descuento = self._estrategia.calcular_descuento(subtotal)
        return subtotal - descuento
Trazabilidad: python_farma/patrones/strategy/i_estrategia_descuento.py, venta_service.py

US-TECH-005: Implementar Registry Pattern para Servicios
Como arquitecto de software Quiero un registro centralizado (Service Locator) para servicios clave Para desacoplar las clases del conocimiento de instanciación de servicios

Criterios de Aceptacion
[x] La clase RegistroServicios debe ser un Singleton (ver US-TECH-001).

[x] Debe tener un diccionario interno _servicios.

[x] Método registrar_servicio(nombre: str, servicio: object).

[x] Método get_servicio(nombre: str) -> object.

[x] Lanzar ValueError si el servicio no está registrado.

Detalles Tecnicos
Clase: RegistroServicios Patrón: Registry (implementado como Singleton)

Implementacion:

Python

import threading

class RegistroServicios:
    _instance = None
    _lock = threading.Lock()

    @classmethod
    def get_instance(cls):
        # (Implementacion Singleton omitida por brevedad - ver US-TECH-001)
        if cls._instance is None:
             with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._servicios = {} # Inicializa el registro
        return cls._instance

    def registrar_servicio(self, nombre: str, servicio: object) -> None:
        self._servicios[nombre] = servicio
        print(f"Servicio '{nombre}' registrado.")

    def get_servicio(self, nombre: str) -> object:
        servicio = self._servicios.get(nombre)
        if not servicio:
            raise ValueError(f"Servicio no registrado: {nombre}")
        return servicio