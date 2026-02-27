"""
Módulo que implementa la cinta de la Máquina de Turing.
"""

class Tape:
    """Representa la cinta infinita de una Máquina de Turing."""
    
    def __init__(self, input_string: str = "", blank_symbol: str = "_"):
        """
        Inicializa la cinta con una cadena de entrada.
        
        Args:
            input_string: Cadena inicial en la cinta
            blank_symbol: Símbolo que representa el blanco
        """
        self.blank = blank_symbol
        self.cells = {}
        
        # Escribir la cadena de entrada en la cinta
        for i, symbol in enumerate(input_string):
            self.cells[i] = symbol
    
    def read(self, position: int) -> str:
        """Lee el símbolo en la posición dada."""
        return self.cells.get(position, self.blank)
    
    def write(self, position: int, symbol: str):
        """Escribe un símbolo en la posición dada."""
        if symbol == self.blank:
            self.cells.pop(position, None)
        else:
            self.cells[position] = symbol
    
    def get_bounds(self) -> tuple:
        """Retorna los límites (mínimo, máximo) de las posiciones usadas."""
        if not self.cells:
            return (0, 0)
        return (min(self.cells.keys()), max(self.cells.keys()))
    
    def get_content(self, margin: int = 2) -> tuple:
        """
        Obtiene el contenido de la cinta como string.
        
        Args:
            margin: Celdas adicionales de blanco a mostrar en los extremos
        
        Returns:
            Tupla (contenido, offset) donde offset es la posición del primer carácter
        """
        if not self.cells:
            return (self.blank * (2 * margin + 1), -margin)
        
        min_pos, max_pos = self.get_bounds()
        start = min_pos - margin
        end = max_pos + margin
        
        content = ""
        for i in range(start, end + 1):
            content += self.read(i)
        
        return (content, start)
    
    def __str__(self) -> str:
        """Representación string de la cinta."""
        content, _ = self.get_content()
        return content.strip(self.blank) or self.blank
