from mbr import Lexer
import json



if __name__ == "__main__":

    with open("rules.txt", mode="r", encoding="utf-8") as f:
        content = f.read()
        
        lex = Lexer.Lexer(content)
        
        print(json.dumps(lex._objects, ensure_ascii=False, indent='\t'))
        
        
        
    #print(lex)