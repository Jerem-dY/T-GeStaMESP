import mbr


if __name__ == "__main__":

    tokenizer = mbr.Compiler(["rules1.txt", "rules2.txt"])
    
    tokenizer.save("test")
    
    ruleset = mbr.Compiler.load("test.mbr")
    
    
    with open("texte_ref.txt", mode="r", encoding="utf-8") as f:
        interp = mbr.Interpreter(ruleset, f.read())
        
        
    """for node in interp._master_node.children:
        print(node.concat())"""
        
    
    chunker = mbr.Compiler(["texte_ref/lexique.txt", "texte_ref/règles.txt"])
    
    with open("texte_ref.txt", mode="r", encoding="utf-8") as f:
        chunks = mbr.Interpreter(chunker, [i.concat() for i in interp._master_node.children], case_sensitive = False)
    
    
    for node in chunks._master_node.children:
        print(node.concat(' '))