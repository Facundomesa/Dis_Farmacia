class FarmaciaException(Exception):
    """Excepción base para errores de la aplicación."""
    def __init__(self, mensaje: str):
        self.mensaje = mensaje
        super().__init__(self.mensaje)