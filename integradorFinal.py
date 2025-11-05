"""
INTEGRADOR FINAL - CONSOLIDACION COMPLETA DEL PROYECTO
============================================================================
Proyecto: PythonFarma
Directorio raiz: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia
Fecha de generacion: 2025-11-05 10:11:11
Total de archivos integrados: 30
Total de directorios procesados: 12
============================================================================
"""

# ==============================================================================
# TABLA DE CONTENIDOS
# ==============================================================================

# DIRECTORIO: .
#   1. buscar_paquete.py
#
# DIRECTORIO: python_farma
#   2. __init__.py
#   3. constantes.py
#
# DIRECTORIO: python_farma\config
#   4. __init__.py
#   5. configuracion.py
#
# DIRECTORIO: python_farma\entidades
#   6. __init__.py
#   7. cliente.py
#   8. producto.py
#   9. tipos_producto.py
#
# DIRECTORIO: python_farma\excepciones
#   10. __init__.py
#   11. farmacia_excepcion.py
#   12. persistencia_excepcion.py
#   13. stock_insuficiente_excepcion.py
#
# DIRECTORIO: python_farma\patrones
#   14. __init__.py
#
# DIRECTORIO: python_farma\patrones\factory
#   15. __init__.py
#   16. producto_factory.py
#
# DIRECTORIO: python_farma\patrones\observer
#   17. __init__.py
#   18. observable.py
#   19. observer.py
#
# DIRECTORIO: python_farma\patrones\registry
#   20. __init__.py
#   21. registros_servicios.py
#
# DIRECTORIO: python_farma\patrones\strategy
#   22. __init__.py
#   23. i_estrategia_descuento.py
#
# DIRECTORIO: python_farma\patrones\strategy\implementacion
#   24. __init__.py
#   25. estrategias_descuento.py
#
# DIRECTORIO: python_farma\services
#   26. __init__.py
#   27. inventario_service.py
#   28. notificador_stock_bajo.py
#   29. persistencia_service.py
#   30. venta_service.py
#



################################################################################
# DIRECTORIO: .
################################################################################

# ==============================================================================
# ARCHIVO 1/30: buscar_paquete.py
# Directorio: .
# Ruta completa: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\buscar_paquete.py
# ==============================================================================

"""
Script para buscar el paquete python_farma desde el directorio raiz del proyecto.
Incluye funcionalidad para integrar archivos Python en cada nivel del arbol de directorios.
"""
import os
import sys
from datetime import datetime


def buscar_paquete(directorio_raiz: str, nombre_paquete: str) -> list:
    """
    Busca un paquete Python en el directorio raiz y subdirectorios.

    Args:
        directorio_raiz: Directorio desde donde iniciar la busqueda
        nombre_paquete: Nombre del paquete a buscar

    Returns:
        Lista de rutas donde se encontro el paquete
    """
    paquetes_encontrados = []

    for raiz, directorios, archivos in os.walk(directorio_raiz):
        # Verificar si el directorio actual es el paquete buscado
        nombre_dir = os.path.basename(raiz)

        if nombre_dir == nombre_paquete:
            # Verificar que sea un paquete Python (contiene __init__.py)
            if '__init__.py' in archivos:
                paquetes_encontrados.append(raiz)
                print(f"[+] Paquete encontrado: {raiz}")
            else:
                print(f"[!] Directorio encontrado pero no es un paquete Python: {raiz}")

    return paquetes_encontrados


def obtener_archivos_python(directorio: str) -> list:
    """
    Obtiene todos los archivos Python en un directorio (sin recursion).

    Args:
        directorio: Ruta del directorio a examinar

    Returns:
        Lista de rutas completas de archivos .py
    """
    archivos_python = []
    
    # Lista de archivos a excluir de la integración
    # Se excluyen los integradores y el main.py
    archivos_excluidos = ['integrador.py', 'integradorFinal.py', 'integrador_farma.py', 'main.py']
    
    try:
        for item in os.listdir(directorio):
            ruta_completa = os.path.join(directorio, item)
            if os.path.isfile(ruta_completa) and item.endswith('.py'):
                # Excluir archivos integradores para evitar recursion infinita
                if item not in archivos_excluidos:
                    archivos_python.append(ruta_completa)
    except PermissionError:
        print(f"[!] Sin permisos para leer: {directorio}")

    return sorted(archivos_python)


def obtener_subdirectorios(directorio: str) -> list:
    """
    Obtiene todos los subdirectorios inmediatos de un directorio.

    Args:
        directorio: Ruta del directorio a examinar

    Returns:
        Lista de rutas completas de subdirectorios
    """
    subdirectorios = []
    try:
        for item in os.listdir(directorio):
            ruta_completa = os.path.join(directorio, item)
            if os.path.isdir(ruta_completa):
                # Excluir directorios especiales
                if not item.startswith('.') and item not in ['__pycache__', 'venv', '.venv', 'data']:
                    subdirectorios.append(ruta_completa)
    except PermissionError:
        print(f"[!] Sin permisos para leer: {directorio}")

    return sorted(subdirectorios)


def leer_contenido_archivo(ruta_archivo: str) -> str:
    """
    Lee el contenido de un archivo Python.

    Args:
        ruta_archivo: Ruta completa del archivo

    Returns:
        Contenido del archivo como string
    """
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            return archivo.read()
    except Exception as error:
        print(f"[!] Error al leer {ruta_archivo}: {error}")
        return f"# Error al leer este archivo: {error}\n"


def crear_archivo_integrador(directorio: str, archivos_python: list) -> bool:
    """
    Crea un archivo integrador.py con el contenido de todos los archivos Python.

    Args:
        directorio: Directorio donde crear el archivo integrador
        archivos_python: Lista de rutas de archivos Python a integrar

    Returns:
        True si se creo exitosamente, False en caso contrario
    """
    if not archivos_python:
        return False

    ruta_integrador = os.path.join(directorio, 'integrador.py')

    try:
        with open(ruta_integrador, 'w', encoding='utf-8') as integrador:
            # Encabezado
            integrador.write('"""\n')
            integrador.write(f"Archivo integrador generado automaticamente\n")
            integrador.write(f"Directorio: {directorio}\n")
            integrador.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            integrador.write(f"Total de archivos integrados: {len(archivos_python)}\n")
            integrador.write('"""\n\n')

            # Integrar cada archivo
            for idx, archivo in enumerate(archivos_python, 1):
                nombre_archivo = os.path.basename(archivo)
                integrador.write(f"# {'=' * 80}\n")
                integrador.write(f"# ARCHIVO {idx}/{len(archivos_python)}: {nombre_archivo}\n")
                integrador.write(f"# Ruta: {archivo}\n")
                integrador.write(f"# {'=' * 80}\n\n")

                contenido = leer_contenido_archivo(archivo)
                integrador.write(contenido)
                integrador.write("\n\n")

            print(f"[OK] Integrador creado: {ruta_integrador}")
            print(f"     Archivos integrados: {len(archivos_python)}")
            return True

    except Exception as error:
        print(f"[!] Error al crear integrador en {directorio}: {error}")
        return False


def procesar_directorio_recursivo(directorio: str, nivel: int = 0, archivos_totales: list = None) -> list:
    """
    Procesa un directorio de forma recursiva, creando integradores en cada nivel.
    Utiliza DFS (Depth-First Search) para llegar primero a los niveles mas profundos.

    Args:
        directorio: Directorio a procesar
        nivel: Nivel de profundidad actual (para logging)
        archivos_totales: Lista acumulativa de todos los archivos procesados

    Returns:
        Lista de todos los archivos Python procesados en el arbol
    """
    if archivos_totales is None:
        archivos_totales = []

    indentacion = "  " * nivel
    print(f"{indentacion}[INFO] Procesando nivel {nivel}: {os.path.basename(directorio)}")

    # Obtener subdirectorios
    subdirectorios = obtener_subdirectorios(directorio)

    # Primero, procesar recursivamente todos los subdirectorios (DFS)
    for subdir in subdirectorios:
        procesar_directorio_recursivo(subdir, nivel + 1, archivos_totales)

    # Despues de procesar subdirectorios, procesar archivos del nivel actual
    archivos_python = obtener_archivos_python(directorio)

    if archivos_python:
        print(f"{indentacion}[+] Encontrados {len(archivos_python)} archivo(s) Python")
        crear_archivo_integrador(directorio, archivos_python)
        # Agregar archivos a la lista total
        archivos_totales.extend(archivos_python)
    else:
        print(f"{indentacion}[INFO] No hay archivos Python en este nivel")

    return archivos_totales


def crear_integrador_final(directorio_raiz: str, archivos_totales: list) -> bool:
    """
    Crea un archivo integradorFinal.py con TODO el codigo fuente de todas las ramas.

    Args:
        directorio_raiz: Directorio donde crear el archivo integrador final
        archivos_totales: Lista completa de todos los archivos Python procesados

    Returns:
        True si se creo exitosamente, False en caso contrario
    """
    if not archivos_totales:
        print("[!] No hay archivos para crear el integrador final")
        return False

    ruta_integrador_final = os.path.join(directorio_raiz, 'integradorFinal.py')

    # Organizar archivos por directorio para mejor estructura
    archivos_por_directorio = {}
    for archivo in archivos_totales:
        directorio = os.path.dirname(archivo)
        if directorio not in archivos_por_directorio:
            archivos_por_directorio[directorio] = []
        archivos_por_directorio[directorio].append(archivo)

    try:
        with open(ruta_integrador_final, 'w', encoding='utf-8') as integrador_final:
            # Encabezado principal
            integrador_final.write('"""\n')
            integrador_final.write("INTEGRADOR FINAL - CONSOLIDACION COMPLETA DEL PROYECTO\n")
            integrador_final.write("=" * 76 + "\n")
            integrador_final.write(f"Proyecto: PythonFarma\n")
            integrador_final.write(f"Directorio raiz: {directorio_raiz}\n")
            integrador_final.write(f"Fecha de generacion: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            integrador_final.write(f"Total de archivos integrados: {len(archivos_totales)}\n")
            integrador_final.write(f"Total de directorios procesados: {len(archivos_por_directorio)}\n")
            integrador_final.write("=" * 76 + "\n")
            integrador_final.write('"""\n\n')

            # Tabla de contenidos
            integrador_final.write("# " + "=" * 78 + "\n")
            integrador_final.write("# TABLA DE CONTENIDOS\n")
            integrador_final.write("# " + "=" * 78 + "\n\n")

            contador_global = 1
            for directorio in sorted(archivos_por_directorio.keys()):
                dir_relativo = os.path.relpath(directorio, directorio_raiz)
                integrador_final.write(f"# DIRECTORIO: {dir_relativo}\n")
                for archivo in sorted(archivos_por_directorio[directorio]):
                    nombre_archivo = os.path.basename(archivo)
                    integrador_final.write(f"#   {contador_global}. {nombre_archivo}\n")
                    contador_global += 1
                integrador_final.write("#\n")

            integrador_final.write("\n\n")

            # Contenido completo organizado por directorio
            contador_global = 1
            for directorio in sorted(archivos_por_directorio.keys()):
                dir_relativo = os.path.relpath(directorio, directorio_raiz)

                # Separador de directorio
                integrador_final.write("\n" + "#" * 80 + "\n")
                integrador_final.write(f"# DIRECTORIO: {dir_relativo}\n")
                integrador_final.write("#" * 80 + "\n\n")

                # Procesar cada archivo del directorio
                for archivo in sorted(archivos_por_directorio[directorio]):
                    nombre_archivo = os.path.basename(archivo)

                    integrador_final.write(f"# {'=' * 78}\n")
                    integrador_final.write(f"# ARCHIVO {contador_global}/{len(archivos_totales)}: {nombre_archivo}\n")
                    integrador_final.write(f"# Directorio: {dir_relativo}\n")
                    integrador_final.write(f"# Ruta completa: {archivo}\n")
                    integrador_final.write(f"# {'=' * 78}\n\n")

                    contenido = leer_contenido_archivo(archivo)
                    integrador_final.write(contenido)
                    integrador_final.write("\n\n")

                    contador_global += 1

            # Footer
            integrador_final.write("\n" + "#" * 80 + "\n")
            integrador_final.write("# FIN DEL INTEGRADOR FINAL\n")
            integrador_final.write(f"# Total de archivos: {len(archivos_totales)}\n")
            integrador_final.write(f"# Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            integrador_final.write("#" * 80 + "\n")

        print(f"\n[OK] Integrador final creado: {ruta_integrador_final}")
        print(f"     Total de archivos integrados: {len(archivos_totales)}")
        print(f"     Total de directorios procesados: {len(archivos_por_directorio)}")

        # Mostrar tamanio del archivo
        tamanio = os.path.getsize(ruta_integrador_final)
        if tamanio < 1024:
            tamanio_str = f"{tamanio} bytes"
        elif tamanio < 1024 * 1024:
            tamanio_str = f"{tamanio / 1024:.2f} KB"
        else:
            tamanio_str = f"{tamanio / (1024 * 1024):.2f} MB"
        print(f"     Tamanio del archivo: {tamanio_str}")

        return True

    except Exception as error:
        print(f"[!] Error al crear integrador final: {error}")
        return False


def integrar_arbol_directorios(directorio_raiz: str) -> None:
    """
    Inicia el proceso de integracion para todo el arbol de directorios.

    Args:
        directorio_raiz: Directorio raiz desde donde comenzar
    """
    print("\n" + "=" * 80)
    print("INICIANDO INTEGRACION DE ARCHIVOS PYTHON")
    print("=" * 80)
    print(f"Directorio raiz: {directorio_raiz}\n")

    # Procesar directorios y obtener lista de todos los archivos
    archivos_totales = procesar_directorio_recursivo(directorio_raiz)

    print("\n" + "=" * 80)
    print("INTEGRACION POR NIVELES COMPLETADA")
    print("=" * 80)

    # Crear integrador final con todos los archivos
    if archivos_totales:
        print("\n" + "=" * 80)
        print("CREANDO INTEGRADOR FINAL")
        print("=" * 80)
        crear_integrador_final(directorio_raiz, archivos_totales)

    print("\n" + "=" * 80)
    print("PROCESO COMPLETO FINALIZADO")
    print("=" * 80)


def main():
    """Funcion principal del script."""
    # Obtener el directorio raiz del proyecto (donde esta este script)
    directorio_raiz = os.path.dirname(os.path.abspath(__file__))

    # Verificar argumentos de linea de comandos
    if len(sys.argv) > 1:
        comando = sys.argv[1].lower()

        if comando == "integrar":
            # Modo de integracion de archivos
            if len(sys.argv) > 2:
                directorio_objetivo = sys.argv[2]
                if not os.path.isabs(directorio_objetivo):
                    directorio_objetivo = os.path.join(directorio_raiz, directorio_objetivo)
            else:
                # Por defecto, integra el directorio raiz actual
                directorio_objetivo = directorio_raiz

            if not os.path.isdir(directorio_objetivo):
                print(f"[!] El directorio no existe: {directorio_objetivo}")
                return 1

            integrar_arbol_directorios(directorio_objetivo)
            return 0

        elif comando == "help" or comando == "--help" or comando == "-h":
            print("Uso: python integrador_farma.py [COMANDO] [OPCIONES]")
            print("")
            print("Comandos disponibles:")
            print("  (sin argumentos)     Busca el paquete 'python_farma'")
            print("  integrar [DIR]       Integra archivos Python en el arbol de directorios")
            print("                       DIR: directorio raiz (por defecto: directorio actual)")
            print("  help                 Muestra esta ayuda")
            print("")
            print("Ejemplos:")
            print("  python integrador_farma.py")
            print("  python integrador_farma.py integrar")
            print("  python integrador_farma.py integrar python_farma")
            return 0

        else:
            print(f"[!] Comando desconocido: {comando}")
            print("    Use 'python integrador_farma.py help' para ver los comandos disponibles")
            return 1

    # Modo por defecto: buscar paquete
    print(f"[INFO] Buscando desde: {directorio_raiz}")
    print(f"[INFO] Buscando paquete: python_farma")
    print("")

    # Buscar el paquete
    paquetes = buscar_paquete(directorio_raiz, "python_farma")

    print("")
    if paquetes:
        print(f"[OK] Se encontraron {len(paquetes)} paquete(s):")
        for paquete in paquetes:
            print(f"  - {paquete}")

            # Mostrar estructura basica del paquete
            print(f"    Contenido:")
            try:
                contenido = os.listdir(paquete)
                for item in sorted(contenido)[:10]:  # Mostrar primeros 10 items
                    ruta_item = os.path.join(paquete, item)
                    if os.path.isdir(ruta_item):
                        print(f"      [DIR]  {item}")
                    else:
                        print(f"      [FILE] {item}")
                if len(contenido) > 10:
                    print(f"      ... y {len(contenido) - 10} items mas")
            except PermissionError:
                print(f"      [!] Sin permisos para leer el directorio")
    else:
        print("[!] No se encontro el paquete python_farma")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())



################################################################################
# DIRECTORIO: python_farma
################################################################################

# ==============================================================================
# ARCHIVO 2/30: __init__.py
# Directorio: python_farma
# Ruta completa: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\python_farma\__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 3/30: constantes.py
# Directorio: python_farma
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
# DIRECTORIO: python_farma\config
################################################################################

# ==============================================================================
# ARCHIVO 4/30: __init__.py
# Directorio: python_farma\config
# Ruta completa: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\python_farma\config\__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 5/30: configuracion.py
# Directorio: python_farma\config
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
# DIRECTORIO: python_farma\entidades
################################################################################

# ==============================================================================
# ARCHIVO 6/30: __init__.py
# Directorio: python_farma\entidades
# Ruta completa: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\python_farma\entidades\__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 7/30: cliente.py
# Directorio: python_farma\entidades
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
# Directorio: python_farma\entidades
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
# Directorio: python_farma\entidades
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
# DIRECTORIO: python_farma\excepciones
################################################################################

# ==============================================================================
# ARCHIVO 10/30: __init__.py
# Directorio: python_farma\excepciones
# Ruta completa: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\python_farma\excepciones\__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 11/30: farmacia_excepcion.py
# Directorio: python_farma\excepciones
# Ruta completa: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\python_farma\excepciones\farmacia_excepcion.py
# ==============================================================================

class FarmaciaException(Exception):
    """Excepción base para errores de la aplicación."""
    def __init__(self, mensaje: str):
        self.mensaje = mensaje
        super().__init__(self.mensaje)

# ==============================================================================
# ARCHIVO 12/30: persistencia_excepcion.py
# Directorio: python_farma\excepciones
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
# Directorio: python_farma\excepciones
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
# DIRECTORIO: python_farma\patrones
################################################################################

# ==============================================================================
# ARCHIVO 14/30: __init__.py
# Directorio: python_farma\patrones
# Ruta completa: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\python_farma\patrones\__init__.py
# ==============================================================================




################################################################################
# DIRECTORIO: python_farma\patrones\factory
################################################################################

# ==============================================================================
# ARCHIVO 15/30: __init__.py
# Directorio: python_farma\patrones\factory
# Ruta completa: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\python_farma\patrones\factory\__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 16/30: producto_factory.py
# Directorio: python_farma\patrones\factory
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
# DIRECTORIO: python_farma\patrones\observer
################################################################################

# ==============================================================================
# ARCHIVO 17/30: __init__.py
# Directorio: python_farma\patrones\observer
# Ruta completa: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\python_farma\patrones\observer\__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 18/30: observable.py
# Directorio: python_farma\patrones\observer
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
# Directorio: python_farma\patrones\observer
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
# DIRECTORIO: python_farma\patrones\registry
################################################################################

# ==============================================================================
# ARCHIVO 20/30: __init__.py
# Directorio: python_farma\patrones\registry
# Ruta completa: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\python_farma\patrones\registry\__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 21/30: registros_servicios.py
# Directorio: python_farma\patrones\registry
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
# DIRECTORIO: python_farma\patrones\strategy
################################################################################

# ==============================================================================
# ARCHIVO 22/30: __init__.py
# Directorio: python_farma\patrones\strategy
# Ruta completa: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\python_farma\patrones\strategy\__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 23/30: i_estrategia_descuento.py
# Directorio: python_farma\patrones\strategy
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
# DIRECTORIO: python_farma\patrones\strategy\implementacion
################################################################################

# ==============================================================================
# ARCHIVO 24/30: __init__.py
# Directorio: python_farma\patrones\strategy\implementacion
# Ruta completa: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\python_farma\patrones\strategy\implementacion\__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 25/30: estrategias_descuento.py
# Directorio: python_farma\patrones\strategy\implementacion
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
# DIRECTORIO: python_farma\services
################################################################################

# ==============================================================================
# ARCHIVO 26/30: __init__.py
# Directorio: python_farma\services
# Ruta completa: C:\Users\Facundo\Desktop\Facundo Tareas\Dis_Farmacia\python_farma\services\__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 27/30: inventario_service.py
# Directorio: python_farma\services
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
# Directorio: python_farma\services
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
# Directorio: python_farma\services
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
# Directorio: python_farma\services
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
# Generado: 2025-11-05 10:11:11
################################################################################
