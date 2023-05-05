from typing import TextIO
import sys


class Logger:

    def __init__(self, file: TextIO = sys.stdout):
        
        self._output = file
        self._prefix = ""
        
    
    def print(self, msg: str, escape: bool = True):
    
        if self._output != None:
            self._output.write(self._prefix + ' ' + msg + '\n')
            

    def title(self, title: str, dot: str = "#", closure=False):
    
        if self._output != None:
            self._output.write(('\n\n' if closure else '') + dot*5 + '\t' + title + '\t' + dot*5 + ('\n' if closure else '\n\n'))
    
    @property
    def prefix(self):
        return self._prefix
        
    @prefix.setter
    def prefix(self, s: str):
        self._prefix = s


SILENT_LOG = Logger(file=None)
DEFAULT_LOG = Logger(file=sys.stdout)
ERROR_LOG = Logger(file=sys.stderr)