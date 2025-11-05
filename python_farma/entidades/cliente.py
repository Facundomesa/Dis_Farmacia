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