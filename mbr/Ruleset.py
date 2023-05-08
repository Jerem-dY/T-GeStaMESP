"""
Ce module définit la classe Ruleset, qui s'attache à compléter les règles et les rendre utilisables.
"""

from .Linker import Linker
from .Logger import Logger, DEFAULT_LOG
from .Parser import unescape
from .Data import OTHER_


class Ruleset:

    def __init__(self, symbol_table: Linker, log: Logger = DEFAULT_LOG):
    
        self._rules = {}
        
        for obj in symbol_table['func']: # Pour chaque fonction :
        
        
            self._rules[obj] = {}

            for premise in symbol_table['func'][obj]['expr']: # Pour chaque expression dans le corps de la fonction :

                if premise in symbol_table['set']:
                
                
                    for val in symbol_table['set'][premise]:
                    
                        val = unescape(val)
                
                        # On ajoute chaque élément du set
                        self._rules[obj][val] = symbol_table['func'][obj]['expr'][premise]
                    
                elif premise == '@':
                    self._rules[obj][OTHER_] = symbol_table['func'][obj]['expr'][premise]
                    
                else:
                    # Si le set n'est pas présent dans les symboles ou qu'il s'agit d'une fonction :
                    raise ValueError(f"Ce set n'existe pas : {premise}")
