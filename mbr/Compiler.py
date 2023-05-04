from mbr import Lexer, Linker, Ruleset, Logger
import json
import pickle


class Compiler:

    def __init__(self, files: list[str], log: Logger.Logger = Logger.DEFAULT_LOG, entry_point: str = ""):

        lex = []
        
        for source in files:
        
            with open(source, mode="r", encoding= "utf-8") as f:
                lex.append(Lexer.Lexer(f.read(), log))

        ld = Linker.Linker(lex, log, entry_point)

        rs = Ruleset.Ruleset(ld, log)
        
        self._ruleset = rs._rules
        
        
    def save(self, filename: str):
    
        if filename[:-4] != "mbr":
            filename += ".mbr"
            
        with open(filename, mode="wb") as f:
            pickle.dump(self, f)
    
    @classmethod    
    def load(cls, filename):
        with open(filename, mode="rb") as f:
            return pickle.load(f)
        
        
    def __repr__(self):
        return json.dumps(self._ruleset, ensure_ascii=False, indent='\t')
    