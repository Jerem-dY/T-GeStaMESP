from enum import Enum, auto
from .Logger import Logger, DEFAULT_LOG
from .Data import FuncTypes, DataTypes


def escape(txt: str) -> str:
    return txt.replace('\n', '\\n').replace('\t', '\\t').replace('\r', '\\r')
    
def unescape(txt: str) -> str:
    return txt.replace('\\n', '\n').replace('\\t', '\t').replace('\\r', '\r')


class Lexer:
    """Lexer et Parser
    """


    class States(Enum):
        
        EMPTY = 0
        IDENTIFIER = auto()
        LITTERAL = auto()
        FUNC = auto()
        SET = auto()
        COMMENT = auto()
        EXPRESSION = auto()
        


    def __init__(self, txt: str, log: Logger = DEFAULT_LOG):
    
    
        self.log = log
        
        # La pile des états
        self._stack = [Lexer.States.EMPTY]
        
        # La pile des objets
        self._objects = {}
        self._current_obj = None
        
        # type de la fonction
        self._func_type = FuncTypes.THROUGH
        
        # buffers
        self._id_buffer = ""
        self._expression_buffer = ""
        self._litt_value_buffer = ""
        self._litt_char = None
        
        self._lines = 1
        self._start_col = 0
        self._i = 1
        
        for self._i, c in enumerate(txt, start=1):
        
            #self.log.print(self.get_position() + f"\t'{escape(c)}'\t{' | '.join([el.name for el in self._stack if el.name != 'EMPTY' or len(self._stack) <= 1])}")

            match self._stack[-1]:
            
                # Quand la pile est vide (aucun objet en cours de construction)
                case Lexer.States.EMPTY:
                    
                    match c:
                    
                        case '#': # Détection des commentaires
                            self._stack.append(Lexer.States.COMMENT)
                            self.log.print(self.get_position() + f">\tCommentaire ouvert.")
                            
                        case c if c.isalnum(): # Détection des identifiants
                            self._stack.append(Lexer.States.IDENTIFIER)
                            self._id_buffer += c
                            self.log.print(self.get_position() + f">\tIdentifiant ouvert.")
                            
                            
                        case '\n' | '\t' | ' ':
                            pass
                            
                        case _:
                            raise SyntaxError(self.get_position() + f"Undefined token: {c}")
                
                
                # Quand un identifiant d'objet est en cours
                case Lexer.States.IDENTIFIER:
                    
                    match c:
                    
                        case '{': # Détection des fonctions
                            self._stack.append(Lexer.States.FUNC)
                            self._open_object(DataTypes.FUNC)
                            self.log.print(self.get_position() + f">\tFonction ouverte.")
                            
                        case '(': # Détection des sets
                            self._stack.append(Lexer.States.SET)
                            self._open_object(DataTypes.SET)
                            self.log.print(self.get_position() + f">\tSet ouvert.")
                          
                        case '*': # Détection du typage des fonctions
                            self._func_type = self._func_type | FuncTypes.ENTRY_POINT
                            
                        case ':': # Détection du typage des fonctions
                            self._func_type = self._func_type | FuncTypes.END_POINT
                            
                            
                        case c if c.isalnum() or c in {'_'}:
                            self._id_buffer += c
                    
                        case _:
                            raise SyntaxError(self.get_position() + f"Undefined token: {c}")
                
                
                # Quand une chaîne de caractère littérale est en cours
                case Lexer.States.LITTERAL:
                    
                    match c:
                        
                        case self._litt_char:
                            self._stack.pop()
                            self._current_obj.append(self._litt_value_buffer)
                            self._litt_value_buffer = ''
                            self.log.print(self.get_position() + f">\tValeur littérale fermée.")
                            
                        case _:
                            self._litt_value_buffer += c
                
                
                # Quand une fonction est en construction
                case Lexer.States.FUNC:
                    
                    match c:
                    
                        case '#': # Détection des commentaires
                            self._stack.append(Lexer.States.COMMENT)
                            
                        case '}':
                        
                            self._close_object()
                            self.log.print(self.get_position() + f">\tFonction fermée.")
                            
                        case c if c.isalnum() or c in {'@', '.'}: # Détection des expressions
                        
                            self._stack.append(Lexer.States.EXPRESSION)
                            self._expression_buffer = c
                            self.log.print(self.get_position() + f">\tExpression ouverte.")
                            
                        case '\n' | ' ' | '\t':
                            pass
                            
                        case _:
                            raise SyntaxError(self.get_position() + f"Undefined token: {c}")
                
                # Quand un set de valeurs est en construction
                case Lexer.States.SET:
                    
                    match c:
                    
                        case ')':
                            self._close_object()
                            self.log.print(self.get_position() + f">\tSet fermé.")
                            
                        case "'" | '"':
                            self._litt_char = c
                            self._stack.append(Lexer.States.LITTERAL)
                            self.log.print(self.get_position() + f">\tValeur littérale ouverte.")
                            
                            
                        case ' ' | '\n' | '\t':
                            pass
                            
                        case _:
                            raise SyntaxError(self.get_position() + f"Undefined token: {c}")
                
                # Quand on est dans un commentaire
                case Lexer.States.COMMENT:
                
                    match c:
                        
                        case '\n':
                            self._stack.pop()
                            self.log.print(self.get_position() + f">\tCommentaire fermé.")
                            
                            
                case Lexer.States.EXPRESSION:
                
                    match c:
                    
                    
                        case c if c.isalnum() or c in {'=', '.', '^', '%', '_'}: # Détection d'un caractère d'expression
                            self._expression_buffer += c
                    
                        case '\n' | ';': # Détection d'un caractère de fin d'expression
                            self._close_expression()
                            self.log.print(self.get_position() + f">\tExpression fermée.")
                            
                        case '}': # Détection d'un caractère de fin d'expression ET de fin de fonction
                            self._close_expression()
                            self.log.print(self.get_position() + f">\tExpression fermée.")
                            
                            self._close_object()
                            self.log.print(self.get_position() + f">\tFonction fermée.")
                            
                            
                        case '\t' | ' ':
                            pass
                            
                        case _:
                            raise SyntaxError(self.get_position() + f"Undefined token: {c}")
                            
            if c == '\n':
                self._lines += 1
                self._start_col = self._i
    
    
    
    def _open_object(self, type: DataTypes):
    
        if type == DataTypes.FUNC:
            self._current_obj = {'mode' : self._func_type, 'expr' : {}}
            self._func_type = FuncTypes.THROUGH
        else:
            self._current_obj = []
    
    
    def _close_expression(self):
        
        state = self._stack.pop()
        
        expr = self._expression_buffer.split('=')

        self._current_obj['expr'][expr[0]] = expr[1]
    
    
    def _close_object(self):
    
        state = self._stack.pop()
        
        if self._stack[-1] == Lexer.States.IDENTIFIER:
            self._stack.pop()
        
        name = self._id_buffer
        self._objects[name] = self._current_obj
        self._id_buffer = ""
        
        self.log.print(f"Objet : '{name}'")


    def get_position(self):
        
        return f"{self._lines:03}:{self._i-self._start_col:03}]"
        
        
    def __iter__(self):
        return iter(self._objects)
        
    def __getitem__(self, item: str):
        return self._objects[item]