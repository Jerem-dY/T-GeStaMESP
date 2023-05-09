from .Logger import Logger
from .Interpreter import MultipassInterpreter, Interpreter
from .Compiler import Compiler



class Chunker:

    def __init__(self, tokenizer: Compiler, passes: list[Compiler], text: str, log: Logger):
    
        self.log = log
        tokens = Interpreter(tokenizer, text, log=self.log)
        self._chunk_tree = MultipassInterpreter(passes, [i.concat() for i in tokens._master_node.children], log=self.log)
        
        
    def list_tokens(self):
        
        s = ""
        for node in self._chunk_tree._master_node.children:
            s += f"[{node.txt:<5}]\t{node.concat(' ')}\n"
            
        return s
            
    def to_xml(self):
    
        return self._chunk_tree._master_node.to_xml()