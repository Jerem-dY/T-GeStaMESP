from mbr.Chunker import Chunker
from mbr.Compiler import Compiler
from mbr.Logger import Logger
import pickle
import glob


if __name__ == "__main__":

    with open("test/output.log", mode="w", encoding="utf-8") as log_file:
        log = Logger(log_file)

        with open("test/texte_ref.txt", mode="r", encoding="utf-8") as f:
        
            chunks = Chunker(
                Compiler.load("test/rulesets/tokenizer.mbr"), # On charge le tokenizer
                [Compiler.load(file) for file in glob.glob("test/rulesets/chunker_pass_?.mbr")], # On charge les différentes passes de règles
                f.read(),
                log
                )

        with open("test/out.xml", mode="w", encoding="utf-8") as out:
            out.write(chunks.to_xml())
            
        with open("test/tokens.tsv", mode="w", encoding="utf-8") as out:
            out.write(chunks.list_tokens())