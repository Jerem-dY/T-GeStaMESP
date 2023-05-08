from .Parser import Parser
from .Data import FuncTypes
from .Logger import Logger, DEFAULT_LOG


class Linker:

    def __init__(self, sources: list[Parser], log: Logger = DEFAULT_LOG,  entry_point = ""):
    
        self._symbols: dict = {'set' : {}, 'func' : {'.' : {'expr' : {}, 'mode' : None}}}
        self._entry_point = ""
        has_end_point = False
        
        for file in sources:
            
            for obj in file:
                
                if obj in self._symbols['func'] or obj in self._symbols['set']:
                    raise ValueError("Doublon trouvé !")
                else:
                
                    if 'mode' in file[obj]:
                    
                        if file[obj]['mode'] & FuncTypes.ENTRY_POINT:
                        
                            log.print(f"FUNC w/ entry_point: {obj}")
                            
                            # Si l'on a déjà un point d'entrée :
                            if self._entry_point != "":
                                if entry_point == obj:
                                    self._entry_point = obj # Si un point d'entrée est spécifié par l'utilisateur, on ignore les autres
                                else:
                                    raise ValueError("plusieurs points d'entrée détectés !")
                            else:
                                self._entry_point = obj
                        
                        elif file[obj]['mode'] & FuncTypes.END_POINT:
                            has_end_point = True
                        
                        self._symbols['func'][obj] = file[obj]
                    else:
                        self._symbols['set'][obj] = file[obj]
                    
        
        if not has_end_point:
            raise ValueError("Pas de point de sortie !")
            
        if self._entry_point == "":
            raise ValueError("Pas de point d'entrée !")
            
            
            
    def __getitem__(self, item: str):
        return self._symbols[item]
        
    def __iter__(self):
        return iter(self._symbols)
