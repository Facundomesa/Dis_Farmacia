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