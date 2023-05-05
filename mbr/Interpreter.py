from .Compiler import Compiler
from .Data import OTHER_
from .Node import Node
from .Logger import Logger, DEFAULT_LOG


class Interpreter:

    def __init__(self, automata: Compiler, tokens: list[str | Node], entry_point: str = None, case_sensitive = True, log: Logger = DEFAULT_LOG):
    
    
        self.log = log
    
        # Mise en place du point d'entrée du programme
        self._previous_state = ""
        self._state = automata._entry_point if entry_point == None else entry_point
        
        
        if automata._entry_point not in automata:
            raise KeyError(f"Le point d'entrée spécifié est introuvable ! {automata._entry_point}")
    
    
        # On prépare les noeuds feuilles :
        nodes = Node.from_list(tokens, True) if not all([isinstance(x, Node) for x in tokens]) else tokens
        self._nodes = [nodes, []]
        self._current_token = None
    
    
        # Pour chaque élément de la liste, on cherche à appliquer les règles définies
        for self._current_token in nodes:
        
            form = self._current_token.txt if case_sensitive else self._current_token.txt.lower()
        
            if form in automata[self._state]:
                self._apply(form, automata)
                
            elif OTHER_ in automata[self._state]:
                self._apply(OTHER_, automata)
                
            else:
                # La prémisse n'est pas valide pour cet état :
                raise ValueError(f"Prémisse '{form}' invalide pour l'état : {self._state}")
     
        self._master_node = Node("MASTER")

        for node in self._nodes[-1]:
            self._master_node.relateAsParent(node)
    
    
    def _apply(self, premise: str, automata: Compiler):
        
        target = automata[self._state][premise]
    
        if automata[self._state][premise][0] == '^':
            no_write = True
            target = target[1:]
        else:
            no_write = False
                
                
        if automata[self._state][premise][0] == '%':
            write_before = True
            target = target[1:]
        else:
            write_before = False
    
    
        self._previous_state = self._state
    
        if target == '.':
            # On reste sur le même état
            target = self._state
            in_place = True
            self.log.print(f"Token : {self._current_token} | State : {self._previous_state} => .")
            
            
        elif target in automata:
            self._state = target
            in_place = False
            self.log.print(f"Token : {self._current_token} | State : {self._previous_state} => {self._state}")
            
        else:
            # Si l'état n'existe pas : Erreur
            raise KeyError(f"Cet état n'existe pas : {automata[self._state][premise]}")
                

        self._write(no_write, write_before, in_place)



    def _write(self, no_write: bool, write_before: bool, in_place: bool):
        

        written = False
            
        if write_before: # Si l'on souhaite écrire avant de changer d'état :
            self._nodes[-1][-1].relateAsParent(self._current_token)
            written = True
        
        
        if not no_write:
            if not in_place:
                self._nodes[-1].append(Node(self._state))
            
            
            if not written: # Si l'on souhaite écrire
                self._nodes[-1][-1].relateAsParent(self._current_token)
            
            
            
        
            
        """if in_place:
            
            if len(self._nodes[-1]) == 0:
                raise ValueError(f"Pas de noeud en cours.")
                
            self._nodes[-1][-1].relateAsParent(self._current_token)
            
        if write_before:
        
            if len(self._nodes[-1]) == 0:
                raise ValueError(f"Pas de noeud en cours.")
                
            self._nodes[-1][-1].relateAsParent(self._current_token)
            self._nodes[-1].append(Node(self._state))
            
        else:
            
            self._nodes[-1].append(Node(self._state))
            self._nodes[-1][-1].relateAsParent(self._current_token)"""