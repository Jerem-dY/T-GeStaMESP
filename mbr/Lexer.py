from enum import Enum, auto
from .Logger import Logger, DEFAULT_LOG
from .Data import FuncTypes


def escape(txt: str) -> str:
    return txt.replace('\n', '\\n').replace('\t', '\\t').replace('\r', '\\r')


class Lexer:


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
        
        # type de la fonction
        func_type = FuncTypes.THROUGH
        
        # buffers
        self._ids = []
        
        self._buffer_objs = []
        self._obj_level = 0
        
        
        for i, c in enumerate(txt):
        
            self.log.print(f"{i:3<}/{len(txt)}\t'{escape(c)}'\t{' | '.join([el.name for el in self._stack if el.name != 'EMPTY' or len(self._stack) <= 1])}")
        
            match self._stack[-1]:
            
                # Quand la pile est vide (aucun objet en cours de construction)
                case Lexer.States.EMPTY:
                    
                    match c:
                    
                        case '#': # Détection des commentaires
                            self._stack.append(Lexer.States.COMMENT)
                            self.log.print(f"{'-'*self._obj_level}>\tCommentaire ouvert.")
                            
                        case c if c.isalnum(): # Détection des identifiants
                            self._stack.append(Lexer.States.IDENTIFIER)
                            self._ids.append(c)
                            self.log.print(f"{'-'*self._obj_level}>\tIdentifiant ouvert.")
                
                
                # Quand un identifiant d'objet est en cours
                case Lexer.States.IDENTIFIER:
                    
                    match c:
                    
                        case '{': # Détection des fonctions
                            self._stack.append(Lexer.States.FUNC)
                            self._open_object()
                            self.log.print(f"{'-'*self._obj_level}>\tFonction ouverte.")
                            
                        case '(': # Détection des sets
                            self._open_object()
                            self._stack.append(Lexer.States.SET)
                            self.log.print(f"{'-'*self._obj_level}>\tSet ouvert.")
                          
                        case '*': # Détection du typage des fonctions
                            func_type = func_type | FuncTypes.ENTRY_POINT
                            
                        case ':': # Détection du typage des fonctions
                            func_type = func_type | FuncTypes.END_POINT
                    
                        case c if c.isalnum():
                            self._ids[-1] += c
                            
                        case c if c.isspace():
                            pass
                
                
                # Quand une chaîne de caractère littérale est en cours
                case Lexer.States.LITTERAL:
                    pass
                
                
                # Quand une fonction est en construction
                case Lexer.States.FUNC:
                    
                    match c:
                    
                        case '#': # Détection des commentaires
                            self._stack.append(Lexer.States.COMMENT)
                            
                        case '}':
                            
                            self.log.print(f"{'-'*self._obj_level}>\tFonction fermée.")
                            
                        case c if c.isalnum() or c in {'@', '.'}: # Détection des expressions
                        
                            self._stack.append(Lexer.States.EXPRESSION)
                            self._open_object()
                            self._ids.append(c)
                            self.log.print(f"{'-'*self._obj_level}>\tExpression ouverte.")
                
                
                # Quand un set de valeurs est en construction
                case Lexer.States.SET:
                    
                    match c:
                    
                        case ')':
                            self._close_object()
                            self.log.print(f"{'-'*self._obj_level}>\tSet fermé.")
                
                # Quand on est dans un commentaire
                case Lexer.States.COMMENT:
                
                    match c:
                        
                        case '\n':
                            self._stack.pop()
                            self.log.print(f"{'-'*self._obj_level}>\tCommentaire fermé.")
                            
                            
                case Lexer.States.EXPRESSION:
                
                    match c:
                    
                    
                        case c if c.isalnum() or c in {'=', '.', '^'}: # Détection d'un caractère d'expression
                            self._ids[-1] += c
                    
                        case '\n' | ';': # Détection d'un caractère de fin d'expression
                            self._close_object()
                            self.log.print(f"{'-'*self._obj_level}>\tExpression fermée.")
                            
                        case '}': # Détection d'un caractère de fin d'expression ET de fin de fonction
                            self._close_object()
                            self.log.print(f"{'-'*self._obj_level}>\tExpression fermée.")
                            
                            self._close_object()
                            self.log.print(f"{'-'*self._obj_level}>\tFonction fermée.")
                            
    
    
    def _open_object(self):
    
        self._obj_level += 1

    def _close_object(self):
    
        state = self._stack.pop()
        
        if self._stack[-1] == Lexer.States.IDENTIFIER:
            self._stack.pop()
        
        name = self._ids.pop()
        

        
        self._obj_level -= 1
        
        self.log.print(f"{'-'*self._obj_level}Buffer : '{self._buffer_objs!r}'")
        
        self.log.print(f"{'-'*self._obj_level}Objet : '{name}'")