import re


texte_support = """
Les signaux étaient assez explicites mais Jérémy espérait se tromper. “ J’avais lu sur Doctissimo que cela faisait partie des symptômes mais je n’ai pas voulu m’alarmer. Les gens se moquaient de moi et me disaient mais non, t’en fais pas, t’es pas Français, t’es juste un peu surmené en ce moment.” témoigne-t-il alors qu’il râle dans les embouteillages.
Mais malheureusement, hier, le couperet tombe, après une prise de sang, Jérémy est positif à la nationalité française, une affection longue durée très handicapante remboursée à 100% par la Sécurité sociale. “ Toute votre vie bascule en un instant, vous savez qu’il y a des choses que vous ne pourrez plus jamais apprécier : un voyage au soleil, un film, un mariage. Vous trouverez toujours quelque chose qui ne va pas. Vous savez que quand on vous demandera “ça va “ vous répondrez désormais des phrases comme “ écoute, on fait comme on peut” nous glisse le primo Français qui broie du noir depuis qu’il a vu la météo ce matin.
Il n’existe aucun traitement pour soigner cette terrible maladie alors que près de 65 millions de personnes sont atteintes de nationalité française. “ Pour l’instant la seule chose qui marche pour les soulager, c’est le vin. Mais ce n’est qu’un soin palliatif qui ne traite pas la cause de la maladie ” déclare le docteur Bernard Moutier lui-même atteint par ce terrible mal.
"""



def cut(chunk: str, mean_size: int = 9) -> list[str]:
   
    out = []
    chunk = chunk.strip()
    
    if len(chunk) >= mean_size:
        size = mean_size-1
        while size < len(chunk) and chunk[size] != ' ':
            size += 1
        
        out.append(chunk[:size])
        if chunk[size:] != '':
            out+= cut(chunk[size:], mean_size)
    elif chunk not in ('\n', ' ', '\t', '\r', ''):
        out.append(chunk)

    return out
pass

def chunkify_length(txt: str, mean_length: int = 9) -> list[str]:

    chunks = re.split(r"( ?[,.:;“”?!]{1} ?)", txt)
    out = []

    for ch in chunks:
        out += cut(ch, mean_length)

    return out
pass


if __name__ == "__main__":


    for i in [4, 9, 10, 11, 12]:

        out = chunkify_length(texte_support.replace("\n", ""), i)

        with open(f"chunked/length/chunkify_length_{i}.txt", mode="w", encoding="utf-8") as f:
            for el in out:
                f.write(el + "\n")