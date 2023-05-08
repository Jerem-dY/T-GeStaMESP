"""
Compilation des règles nécessaires à l'analyse en chunks.
Cela comprend les règles de tokenisation et les règles de découpoage en chunks.
"""


import mbr

if __name__ == "__main__":

    tokenizer = mbr.Compiler(["tokenizer/rules1.txt", "tokenizer/rules2.txt"])
    tokenizer.save("tokenizer")

    chunker = mbr.Compiler(["texte_ref/lexique.txt", "texte_ref/règles.txt"])
    chunker.save("chunker_pass_1")
