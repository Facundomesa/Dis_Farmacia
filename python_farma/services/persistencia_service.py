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