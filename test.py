import mbr


if __name__ == "__main__":

    out = mbr.Compiler(["rules1.txt", "rules2.txt"])
    
    out.save("test")
    
    ruleset = mbr.Compiler.load("test.mbr")
    
    print(ruleset)