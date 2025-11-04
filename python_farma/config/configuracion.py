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