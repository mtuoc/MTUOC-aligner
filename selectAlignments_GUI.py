import sys
import codecs
import unicodedata
import argparse
import os

from tkinter import *
from tkinter.ttk import *

import tkinter 
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from tkinter.filedialog import askdirectory
from tkinter import messagebox

from tkinter import *
from tkinter.ttk import *

import tkinter 
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from tkinter.filedialog import askdirectory
from tkinter import messagebox

def remove_control_characters(s):
    return "".join(ch for ch in s if unicodedata.category(ch)[0]!="C")


'''
parser = argparse.ArgumentParser(description='A script to select aligments in a directory with a higher confidence than the given one into a single file. The alignment file should be a TSV file with three fields: source segment, target segment, confidence score.')
parser.add_argument("-i","--inDir", type=str, help="The input dir containing the hunalign alignments.", required=True)
parser.add_argument("-o","--outFile", type=str, help="The input fule.", required=True)
parser.add_argument("-c","--confidence", type=float, help="The minimun confidence (the output confidence will be highet tnar the one provided..", required=True)


args = parser.parse_args()



        
'''

def select_input_directory():
    dir = askdirectory(initialdir = ".",mustexist=True, title = "Choose the input directory.")
    E1.delete(0,END)
    E1.insert(0,dir)
    E1.xview_moveto(1)
    
def select_output_file():
    outputfile = asksaveasfilename(initialdir = ".",filetypes =(("All Files","*.*"),),
                           title = "Choose the output file.")
    E2.delete(0,END)
    E2.insert(0,outputfile)
    E2.xview_moveto(1)
    
def go():
    dirin=E1.get()
    fout=E2.get()
    confidence=float(E3.get())

    sortida=codecs.open(fout,"w",encoding="utf-8")

    for r, d, f in os.walk(dirin):
        for file in f:
            fullname=os.path.join(dirin,file)
            
            entrada=codecs.open(fullname,"r",encoding="utf-8")

            llistasortida=[]
            iguals=0
            totals=0
            for linia in entrada:
                linia=linia.rstrip().replace("~~~","")
                camps=linia.split("\t")
                L1seg=camps[0].strip()
                L1seg=" ".join(L1seg.split())
                L2seg=camps[1].strip()
                L2seg=" ".join(L2seg.split())
                totals+=1
                if not L1seg=="<p>" and L1seg==L2seg: iguals+=1
                sim=float(camps[2])
                if sim>=confidence and not L1seg=="<p>" and not L1seg=="" and not L2seg=="<p>" and not L2seg=="":
                    L1seg=remove_control_characters(L1seg)
                    L2seg=remove_control_characters(L2seg)
                    if len(L1seg)>0 and len(L2seg)>0:
                        cadena=L1seg+"\t"+L2seg
                        llistasortida.append(cadena)
            try:
                percent=iguals/totals
            except:
                percent=1
            if percent<=0.5:
                for cadena in llistasortida:
                    camps=cadena.split("\t")
                    sl1=camps[0]
                    #print(len(sl1),sl1)
                    sl2=camps[1]
                    toWrite=True
                    if len(sl1)>25 and sl1==sl2:
                        toWrite=False
                    if toWrite:
                        sortida.write(cadena+"\n")

top = Tk()
top.title("selectAlignments_GUI")

B1=tkinter.Button(top, text = str("Input directory"), borderwidth = 1, command=select_input_directory,width=14).grid(row=0,column=0)
E1 = tkinter.Entry(top, bd = 5, width=50, justify="right")
E1.xview_moveto(1)
E1.grid(row=0,column=1)

B2=tkinter.Button(top, text = str("Output file"), borderwidth = 1, command=select_output_file,width=14).grid(row=1,column=0)
E2 = tkinter.Entry(top, bd = 5, width=50, justify="right")
E2.grid(row=1,column=1)

L3 = Label(top,text="Confidence:").grid(sticky="E",row=2,column=0)
E3 = tkinter.Entry(top, bd = 5, width=15, justify="left")
E3.grid(sticky="W",row=2,column=1)

B4=tkinter.Button(top, text = str("Go!"), borderwidth = 1, command=go,width=14).grid(sticky="W",row=6,column=0)

top.mainloop()