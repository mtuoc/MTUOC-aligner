#    MTUOC-autoaligner-hunalign
#    Copyright (C) 2025  Antoni Oliver
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

import tkinter 
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename

import yaml
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
    
import subprocess
import unicodedata
    
###SEGMENTER
import sys
import codecs
import os

#SRX_SEGMENTER
import lxml.etree
import regex
from typing import (
    List,
    Set,
    Tuple,
    Dict,
    Optional
)

import sys

class SrxSegmenter:
    """Handle segmentation with SRX regex format.
    """
    def __init__(self, rule: Dict[str, List[Tuple[str, Optional[str]]]], source_text: str) -> None:
        self.source_text = source_text
        self.non_breaks = rule.get('non_breaks', [])
        self.breaks = rule.get('breaks', [])

    def _get_break_points(self, regexes: List[Tuple[str, str]]) -> Set[int]:
        return set([
            match.span(1)[1]
            for before, after in regexes
            for match in regex.finditer('({})({})'.format(before, after), self.source_text)
        ])

    def get_non_break_points(self) -> Set[int]:
        """Return segment non break points
        """
        return self._get_break_points(self.non_breaks)

    def get_break_points(self) -> Set[int]:
        """Return segment break points
        """
        return self._get_break_points(self.breaks)

    def extract(self) -> Tuple[List[str], List[str]]:
        """Return segments and whitespaces.
        """
        non_break_points = self.get_non_break_points()
        candidate_break_points = self.get_break_points()

        break_point = sorted(candidate_break_points - non_break_points)
        source_text = self.source_text

        segments = []  # type: List[str]
        whitespaces = []  # type: List[str]
        previous_foot = ""
        for start, end in zip([0] + break_point, break_point + [len(source_text)]):
            segment_with_space = source_text[start:end]
            candidate_segment = segment_with_space.strip()
            if not candidate_segment:
                previous_foot += segment_with_space
                continue

            head, segment, foot = segment_with_space.partition(candidate_segment)

            segments.append(segment)
            whitespaces.append('{}{}'.format(previous_foot, head))
            previous_foot = foot
        whitespaces.append(previous_foot)

        return segments, whitespaces


def parse(srx_filepath: str) -> Dict[str, Dict[str, List[Tuple[str, Optional[str]]]]]:
    """Parse SRX file and return it.
    :param srx_filepath: is soruce SRX file.
    :return: dict
    """
    tree = lxml.etree.parse(srx_filepath)
    namespaces = {
        'ns': 'http://www.lisa.org/srx20'
    }

    rules = {}

    for languagerule in tree.xpath('//ns:languagerule', namespaces=namespaces):
        rule_name = languagerule.attrib.get('languagerulename')
        if rule_name is None:
            continue

        current_rule = {
            'breaks': [],
            'non_breaks': [],
        }

        for rule in languagerule.xpath('ns:rule', namespaces=namespaces):
            is_break = rule.attrib.get('break', 'yes') == 'yes'
            rule_holder = current_rule['breaks'] if is_break else current_rule['non_breaks']

            beforebreak = rule.find('ns:beforebreak', namespaces=namespaces)
            beforebreak_text = '' if beforebreak.text is None else beforebreak.text

            afterbreak = rule.find('ns:afterbreak', namespaces=namespaces)
            afterbreak_text = '' if afterbreak.text is None else afterbreak.text

            rule_holder.append((beforebreak_text, afterbreak_text))

        rules[rule_name] = current_rule

    return rules

def remove_control_characters(s):
    return "".join(ch for ch in s if unicodedata.category(ch)[0]!="C")

def segmenta(cadena,rules,srxlang):
    segmenter = SrxSegmenter(rules[srxlang],cadena)
    segments=segmenter.extract()
    resposta=[]
    for segment in segments[0]:
        segment=segment.replace("’","'")
        resposta.append(segment)
    resposta="\n".join(resposta)
    return(resposta)


###GUI    
def select_config_file():
    infile = askopenfilename(initialdir = ".",filetypes =(("yaml files","*.yaml"),("All Files","*.*")),
                           title = "Select the input file.")
    E1.delete(0,END)
    E1.insert(0,infile)
    E1.xview_moveto(1)    
    

def go():
    ###YAML
    if len(sys.argv)==1:
        configfile=E1.get()
    else:
        configfile=sys.argv[1]
    stream = open(configfile, 'r',encoding="utf-8")
    configYAML=yaml.load(stream, Loader=yaml.FullLoader)

    dirSL=configYAML["dirSL"]
    dirTL=configYAML["dirTL"]
    dirALI=configYAML["dirALI"]
    batchfile=configYAML["batchfile"]
    srxfile=configYAML["srxfile"]
    SLname=configYAML["SLname"]
    TLname=configYAML["TLname"]
    paramark=configYAML["paramark"]
    alignmentdictionary=configYAML["alignmentdictionary"]
    r1=configYAML["r1"]
    r2=configYAML["r2"]
    if r1=="None": r1=None
    if r2=="None": r2=None
    minconfidence=float(configYAML["minconfidence"])
    outfile=configYAML["outfile"]
    OperatingSystem=configYAML["OperatingSystem"]
    
    ###SEGMENTING L1
    inDir=dirSL
    SLsegDir=inDir+"-seg"
    if not inDir.endswith("/") and not inDir.endswith("\\"):
        inDir=inDir+"/"
    
    if not SLsegDir.endswith("/") and not SLsegDir.endswith("\\"):
        SLsegDir=SLsegDir+"/"
    if not os.path.exists(SLsegDir):
        os.makedirs(SLsegDir)
    srxlang=SLname
    rules = parse(srxfile)
    languages=list(rules.keys())
    if not srxlang in languages:
        print("Language ",srxlang," not available in ", srxfile)
        print("Available languages:",", ".join(languages))
        sys.exit()
    files = []
    for r, d, f in os.walk(inDir):
        for file in f:
            if file.endswith('.txt'):
                fullpath=os.path.join(r, file)            
                print(fullpath)
                entrada=codecs.open(fullpath,"r",encoding="utf-8",errors="ignore")
                outfile=fullpath.replace(inDir,SLsegDir)
                print(outfile)
                sortida=codecs.open(outfile,"w",encoding="utf-8")
                for linia in entrada:
                    segments=segmenta(linia,rules,srxlang)
                    if len(segments)>0:
                        if paramark: sortida.write("<p>\n")
                        sortida.write(segments+"\n")
                        
    ###SEGMENTING L2
    inDir=dirTL
    TLsegDir=inDir+"-seg"
    if not inDir.endswith("/") and not inDir.endswith("\\"):
        inDir=inDir+"/"
    
    if not TLsegDir.endswith("/") and not TLsegDir.endswith("\\"):
        TLsegDir=TLsegDir+"/"
    if not os.path.exists(TLsegDir):
        os.makedirs(TLsegDir)
    srxlang=TLname
    rules = parse(srxfile)
    languages=list(rules.keys())
    if not srxlang in languages:
        print("Language ",srxlang," not available in ", srxfile)
        print("Available languages:",", ".join(languages))
        sys.exit()
    files = []
    for r, d, f in os.walk(inDir):
        for file in f:
            if file.endswith('.txt'):
                fullpath=os.path.join(r, file)            
                print(fullpath)
                entrada=codecs.open(fullpath,"r",encoding="utf-8",errors="ignore")
                outfile=fullpath.replace(inDir,TLsegDir)
                print(outfile)
                sortida=codecs.open(outfile,"w",encoding="utf-8")
                for linia in entrada:
                    segments=segmenta(linia,rules,srxlang)
                    if len(segments)>0:
                        if paramark: sortida.write("<p>\n")
                        sortida.write(segments+"\n")
                        
    #CREATE BATCH FILE
    dir1=SLsegDir
    dir2=TLsegDir
    dir3=dirALI
    if not os.path.exists(dir3):
        os.makedirs(dir3)
    outfile=batchfile

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
        if not r1==None and not r2==None:
            file2=file1.replace(r1,r2)
        else:
            file2=file1
        
        if file2 in files2:
            dirfile1=os.path.join(dir1, file1)
            dirfile2=os.path.join(dir2, file2)
            fileali="ali-"+file1
            dirfileali=os.path.join(dir3, fileali)
            cadena=dirfile1+"\t"+dirfile2+"\t"+dirfileali
            sortida.write(cadena+"\n")
        else:
            print("***",file1)
    sortida.close()   

    ###ALIGN
    if OperatingSystem=="Windows":
        print("ALIGNING")
        command="hunalign.exe -batch "+alignmentdictionary+" -text -realign -utf "+batchfile
        print(command)
    elif OperatingSystem=="Linux":
        print("ALIGNING")
        command="./hunalign -batch "+alignmentdictionary+" -text -realign -utf "+batchfile
        print(command)    
    
    elif OperatingSystem=="MacOs":
        print("ALIGNING")
        command="./hunalignMAC -batch "+alignmentdictionary+" -text -realign -utf "+batchfile
        print(command)    
        
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print("ALIGNMENT FINISHED")
    #SELECTION
    dirin=dirALI
    outfile=configYAML["outfile"]
    fout=outfile
    confidence=minconfidence

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



if len(sys.argv)==1:
    top = Tk()
    top.title("MTUOC-autoaligner-hunalign")

    B1=tkinter.Button(top, text = str("Select config file"), borderwidth = 1, command=select_config_file,width=14).grid(row=0,column=0)
    E1 = tkinter.Entry(top, bd = 5, width=60, justify="right")
    E1.grid(row=0,column=1)

    E1.delete(0,END)
    E1.insert(0,os.path.join(os.getcwd(), "config.yaml"))

    B2=tkinter.Button(top, text = str("Align!"), borderwidth = 1, command=go,width=14).grid(sticky="W",row=5,column=0)

    top.mainloop()
else:
    go()







