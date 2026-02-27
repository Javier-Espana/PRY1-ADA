"""
Módulo que implementa la Máquina de Turing determinista de una cinta.
"""

from tape import Tape
from loader import get_transition


class TuringMachine:
    """Máquina de Turing determinista de una cinta."""
    
    def __init__(self, config: dict):
        """
        Inicializa la Máquina de Turing con una configuración.
        
        Args:
            config: Diccionario con la configuración de la máquina
        """
        self.config = config
        self.tape = None
        self.head_position = 0
        self.current_state = config['estado_inicial']
        self.halted = False
        self.accepted = False
        self.step_count = 0
        self.history = []
    
    def reset(self, input_string: str = ""):
        """Reinicia la máquina con una nueva entrada."""
        blank = self.config['simbolo_blanco']
        self.tape = Tape(input_string, blank)
        self.head_position = 0
        self.current_state = self.config['estado_inicial']
        self.halted = False
        self.accepted = False
        self.step_count = 0
        self.history = []
        self._save_configuration()
    
    def _save_configuration(self):
        """Guarda la configuración actual en el historial."""
        tape_content, offset = self.tape.get_content(margin=3)
        self.history.append({
            'step': self.step_count,
            'state': self.current_state,
            'head': self.head_position,
            'tape': tape_content,
            'offset': offset
        })
    
    def step(self) -> bool:
        """
        Ejecuta un paso de la máquina.
        
        Returns:
            True si la máquina puede continuar, False si se detuvo
        """
        if self.halted:
            return False
        
        # Leer símbolo actual
        symbol = self.tape.read(self.head_position)
        
        # Obtener transición
        transition = get_transition(self.config, self.current_state, symbol)
        
        if transition is None:
            self.halted = True
            self.accepted = self.current_state in self.config['estados_aceptacion']
            return False
        
        new_state, write_symbol, direction = transition
        
        # Escribir símbolo
        self.tape.write(self.head_position, write_symbol)
        
        # Cambiar estado
        self.current_state = new_state
        
        # Mover cabeza
        if direction == 'R':
            self.head_position += 1
        elif direction == 'L':
            self.head_position -= 1
        # 'S' = sin movimiento
        
        self.step_count += 1
        self._save_configuration()
        
        # Verificar si llegamos a estado de aceptación/rechazo
        if self.current_state in self.config['estados_aceptacion']:
            self.halted = True
            self.accepted = True
        elif self.current_state in self.config.get('estados_rechazo', []):
            self.halted = True
            self.accepted = False
        
        return not self.halted
    
    def run(self, max_steps: int = 100000) -> bool:
        """
        Ejecuta la máquina hasta que se detenga o alcance el límite.
        
        Args:
            max_steps: Número máximo de pasos permitidos
        
        Returns:
            True si la máquina aceptó, False en caso contrario
        """
        while self.step_count < max_steps and self.step():
            pass
        
        return self.accepted
    
    def get_result(self) -> str:
        """Obtiene el resultado (contenido de la cinta)."""
        return str(self.tape)
    
    def get_clean_result(self) -> str:
        """
        Obtiene el resultado limpio (solo los 1s del resultado Fibonacci).
        Para la máquina de cinta única, extrae el último término de la secuencia.
        Formato de cinta: #xxx.;1;1;11;111;... donde el último término es F(n)
        """
        raw = str(self.tape).strip('_')
        
        # Si la cinta contiene ';' (separador de términos), extraer el último término
        if ';' in raw:
            # Dividir por ';' y obtener el penúltimo elemento (último término completo)
            terminos = raw.split(';')
            # Filtrar términos vacíos y obtener el último con 1s
            terminos_validos = [t for t in terminos if t and all(c == '1' for c in t)]
            if terminos_validos:
                return terminos_validos[-1]
        
        # Fallback: solo los '1's en la cinta final
        return ''.join(c for c in raw if c == '1')
