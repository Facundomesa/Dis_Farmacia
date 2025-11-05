from python_farma.excepciones.farmacia_excepcion import FarmaciaException

class PersistenciaException(FarmaciaException):
    """Lanzada cuando falla una operación de serialización (pickle) o I/O."""
    
    def __init__(self, mensaje: str, error_original: Exception | None = None):
        self.error_original = error_original
        mensaje_completo = f"Error de persistencia: {mensaje}"
        if error_original:
            mensaje_completo += f". Error base: {error_original}"
            
        super().__init__(mensaje_completo)