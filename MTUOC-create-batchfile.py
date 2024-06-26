#    MTUOC-create-batchfile
#    Copyright (C) 2024  Antoni Oliver
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
import argparse

parser = argparse.ArgumentParser(description='A script to create the batch file to be used with hunalign.')
parser.add_argument("--dirSL", type=str, help="The input dir containing the segmented text files for the source language.", required=True)
parser.add_argument("--dirTL", type=str, help="The input dir containing the segmented text files for the target language.", required=True)
parser.add_argument("--dirALI", type=str, help="The output dir to save the aligned files.", required=True)
parser.add_argument("--batchfile", type=str, help="The name of the alignment script.", required=True)
parser.add_argument("--r1", type=str, help="The first string for name replacement.", required=False)
parser.add_argument("--r2", type=str, help="The second string for name replacement.", required=False)

args = parser.parse_args()


if args.r1:
    r1=args.r1
else:
    r1=""
if args.r2:
    r2=args.r2
else:
    r2=""

dir1=args.dirSL
dir2=args.dirTL
dir3=args.dirALI
if not os.path.exists(dir3):
    os.makedirs(dir3)
outfile=args.batchfile

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
        dirfile1=os.path.join(dir1, file1)
        dirfile2=os.path.join(dir2, file2)
        fileali="ali-"+file1
        dirfileali=os.path.join(dir3, fileali)
        cadena=dirfile1+"\t"+dirfile2+"\t"+dirfileali
        sortida.write(cadena+"\n")
    else:
        print("***",file1)
sortida.close()       
with open(outfile) as f_input:
    data = f_input.read().rstrip('\n')

with open(outfile, 'w') as f_output:    
    f_output.write(data)
        
