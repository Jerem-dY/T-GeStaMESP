"""
La classe Compiler présente dans ce module s'occupe de gérer la pipeline de traitement nécessaire à 'élaboration de la base de règles, prenant en entrée les différents fichiers source impliqués et permettant une sortie binaire (.mbr) ou en JSON.
"""

from mbr import Parser, Linker, Ruleset, Logger
import json
import pickle


class Compiler:

    def __init__(self, files: list[str], log: Logger.Logger = Logger.DEFAULT_LOG, entry_point: str = ""):

        log.title("DEBUT DE LA COMPILATION", dot='**')

        # Analyse lexicale + parsing
        log.title("LEXER")
        lex = []
        for source in files:
        
            with open(source, mode="r", encoding= "utf-8") as f:
                log.prefix = "['" + source + "'"
                lex.append(Parser.Parser(f.read(), log))


        # Mise en commun des symboles des différents fichiers sources
        log.title("LINKER")
        log.prefix = "[LINKER] "
        ld = Linker.Linker(lex, log, entry_point)

        # Mise en place de la structure de données finale
        rs = Ruleset.Ruleset(ld, log)
        
        self._ruleset = rs._rules
        self._entry_point = ld._entry_point
        
        log.title("FIN DE LA COMPILATION", dot='**', closure=True)
        log.prefix = ""
        
        
    def save(self, filename: str):
    
        if filename[:-4] != "mbr":
            filename += ".mbr"
            
        with open(filename, mode="wb") as f:
            pickle.dump(self, f)
    
    @classmethod    
    def load(cls, filename):
        with open(filename, mode="rb") as f:
            return pickle.load(f)



    def __contains__(self, item):
        return item in self._ruleset
        
    def __getitem__(self, item):
        return self._ruleset[item]
        
    def __iter__(self):
        return iter(self._ruleset)
        
    def __repr__(self):
        return json.dumps(self._ruleset, ensure_ascii=False, indent='\t')
    
