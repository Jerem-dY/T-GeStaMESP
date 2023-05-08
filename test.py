from mbr.Compiler import Compiler
from mbr.Interpreter import Interpreter, MultipassInterpreter


if __name__ == "__main__":


    # Récupération des fichiers de règles
    
    tokenizer = Compiler.load("tokenizer.mbr")
    
    ruleset = Compiler.load("chunker_pass_1.mbr")
    
    with open("texte_ref.txt", mode="r", encoding="utf-8") as f:
        interp = Interpreter(tokenizer, f.read())

    
    with open("texte_ref.txt", mode="r", encoding="utf-8") as f:
        chunk_tree = MultipassInterpreter([ruleset], [i.concat() for i in interp._master_node.children])

    
    for node in chunk_tree._master_node.children:
        print(f"[{node.txt:<5}]\t{node.concat(' ')}")

    print(chunk_tree._master_node.to_xml())
    print("Done !")
