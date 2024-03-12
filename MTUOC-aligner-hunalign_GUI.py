#    MTUOC-aligner-hunalign
#    Copyright (C) 2022  Antoni Oliver
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

#    Segmentation is performed using srx_segmenter: https://github.com/narusemotoki/srx_segmenter
#    The code is copied into this script.

import codecs
import os
import sys


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

def select_SL_directory():
    dir = askdirectory(initialdir = ".",mustexist=True, title = "Choose the directory containing the SL files.")
    E1.delete(0,END)
    E1.insert(0,dir)
    E1.xview_moveto(1)
    
def select_TL_directory():
    outdir = askdirectory(initialdir = ".",mustexist=False, title = "Choose the directory containing the TL files.")
    E2.delete(0,END)
    E2.insert(0,outdir)
    E2.xview_moveto(1)

def select_ALI_directory():
    outdir = askdirectory(initialdir = ".",mustexist=False, title = "Choose the directory where the alignment files will be stored.")
    E3.delete(0,END)
    E3.insert(0,outdir)
    E3.xview_moveto(1)
    
def select_align_script():
    srxfile = asksaveasfilename(initialdir = ".",filetypes =(("All Files","*.*"),),
                           title = "Choose the name for the alignment script.")
    E4.delete(0,END)
    E4.insert(0,srxfile)
    E4.xview_moveto(1)
    
def select_align_dictionary():
    srxfile = askopenfilename(initialdir = ".",filetypes =(("All Files","*.*"),),
                           title = "Choose the alignment directory.")
    E5.delete(0,END)
    E5.insert(0,srxfile)
    E5.xview_moveto(1)
    
def go():
    print("GO!")
    dir1=E1.get()
    dir2=E2.get()
    dir3=E3.get()
    
    outfile=E4.get()
    hundict=E5.get()

    r1=E6.get()
    r2=E7.get()
    
    windows=paragraph.get()
    thisdir = os.getcwd()
    files1=[]
    for r, d, f in os.walk(dir1):
        for file in f:
            files1.append(file)
            
    files2=[]
    for r, d, f in os.walk(dir2):
        for file in f:
            files2.append(file)
    sortida=codecs.open(outfile,"w",encoding="utf-8")

    for file1 in files1:
        file2=file1.replace(r1,r2)
        if file2 in files2:
            fileali="ali-"+file1
            if windows:
                cadena="hunalign.exe "+hundict+" -utf -realign -text \""+dir1+"/"+file1+"\" "+"\""+dir2+"/"+file2+"\" > \""+dir3+"/"+fileali+"\""
            else:
                cadena="timeout 5m ./hunalign "+hundict+" -utf -realign -text \""+dir1+"/"+file1+"\" "+"\""+dir2+"/"+file2+"\" > \""+dir3+"/"+fileali+"\""
            print(cadena)
            sortida.write(cadena+"\n")
        else:
            print("***",file1)

top = Tk()
top.title("MTUOC-aligner-hunalign_GUI")

B1=tkinter.Button(top, text = str("Source lang. dir"), borderwidth = 1, command=select_SL_directory,width=14).grid(row=0,column=0)
E1 = tkinter.Entry(top, bd = 5, width=50, justify="right")
E1.xview_moveto(1)
E1.grid(row=0,column=1)

B2=tkinter.Button(top, text = str("Target lang. dir"), borderwidth = 1, command=select_TL_directory,width=14).grid(row=1,column=0)
E2 = tkinter.Entry(top, bd = 5, width=50, justify="right")
E2.grid(row=1,column=1)

B3=tkinter.Button(top, text = str("Aligned files dir"), borderwidth = 1, command=select_ALI_directory,width=14).grid(row=2,column=0)
E3 = tkinter.Entry(top, bd = 5, width=50, justify="right")
E3.grid(row=2,column=1)

B4=tkinter.Button(top, text = str("Align script"), borderwidth = 1, command=select_align_script,width=14).grid(row=3,column=0)
E4 = tkinter.Entry(top, bd = 5, width=50, justify="right")
E4.grid(row=3,column=1)

B5=tkinter.Button(top, text = str("Align dictionary"), borderwidth = 1, command=select_align_dictionary,width=14).grid(row=4,column=0)
E5 = tkinter.Entry(top, bd = 5, width=50, justify="right")
E5.grid(row=4,column=1)

L6 = Label(top,text="Source lang. ending:").grid(sticky="E",row=5,column=0)
E6 = tkinter.Entry(top, bd = 5, width=15, justify="left")
E6.grid(sticky="W",row=5,column=1)

L7 = Label(top,text="Target lang. ending:").grid(sticky="E",row=6,column=0)
E7 = tkinter.Entry(top, bd = 5, width=15, justify="left")
E7.grid(sticky="W",row=6,column=1)

L8 = Label(top,text="Windows:").grid(sticky="E",row=7,column=0)
paragraph=tkinter.BooleanVar()
cbwindows = tkinter.Checkbutton(top,variable=paragraph, onvalue=True, offvalue=False)
cbwindows.grid(sticky="W",row=7,column=1)

B9=tkinter.Button(top, text = str("Create script!"), borderwidth = 1, command=go,width=14).grid(sticky="W",row=8,column=0)

top.mainloop()