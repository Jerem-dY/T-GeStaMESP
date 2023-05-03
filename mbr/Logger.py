from typing import TextIO
import sys


class Logger:

    def __init__(self, file: TextIO = sys.stdout):
        
        self._output = file
        
    
    def print(self, msg: str, escape: bool = True):
    
        if self._output != None:
        
            self._output.write(msg + '\n')
            

SILENT_LOG = Logger(file=None)
DEFAULT_LOG = Logger(file=sys.stdout)
ERROR_LOG = Logger(file=sys.stderr)