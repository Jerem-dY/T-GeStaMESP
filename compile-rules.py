"""
Compilation des règles nécessaires à l'analyse en chunks.
Cela comprend les règles de tokenisation et les règles de découpage en chunks.
"""


import mbr

if __name__ == "__main__":

    tokenizer = mbr.Compiler(["test/tokenizer/rules1.txt", "test/tokenizer/rules2.txt"])
    tokenizer.save("test/rulesets/tokenizer")

    chunker_p1 = mbr.Compiler(["test/passe1/lexique.txt", "test/passe1/règles.txt"])
    chunker_p1.save("test/rulesets/chunker_pass_1")
