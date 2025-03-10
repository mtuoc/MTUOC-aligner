import codecs
import sys

fentradaX=sys.argv[1]
fentradaY=sys.argv[2]
fsortida=sys.argv[3]

entradaX=codecs.open(fentradaX,"r",encoding="utf-8")
entradaY=codecs.open(fentradaY,"r",encoding="utf-8")

sortida=codecs.open(fsortida,"w",encoding="utf-8")

dicENX={}
dicENY={}

for linia in entradaX:
    linia=linia.strip()
    try:
        (X,en)=linia.split("\t")
        if not en in dicENX:
            dicENX[en]=[]
            dicENX[en].append(X)
        else:
            dicENX[en].append(X)
    except:
        pass
            
for linia in entradaY:
    linia=linia.strip()
    try:
        (Y,en)=linia.split("\t")
        if not en in dicENY:
            dicENY[en]=[]
            dicENY[en].append(Y)
        else:
            dicENY[en].append(Y)
    except:
        pass

for en in dicENX:
    if en in dicENY:
        for X in dicENX[en]:
            for Y in dicENY[en]:
                cadena=Y+" @ "+X
                sortida.write(cadena+"\n")
                