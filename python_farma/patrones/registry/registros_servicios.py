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