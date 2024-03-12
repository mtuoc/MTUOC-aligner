import codecs
import sys

fentrada=sys.argv[1]
fsortida=sys.argv[2]

entrada=codecs.open(fentrada,"r",encoding="utf-8")
sortida=codecs.open(fsortida,"w",encoding="utf-8")

for linia in entrada:
    linia=linia.rstrip()
    try:
        linia=linia.replace("\t"," ")
        camps=linia.split(" ")
        cadena=camps[1].strip()+" @ "+camps[0].strip()
        sortida.write(cadena+"\n")
    except:
        pass
entrada.close()
sortida.close()
