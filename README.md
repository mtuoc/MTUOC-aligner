# MTUOC-aligner
Scripts and programs to automatically align text files using Hunalign or SBERT.

This repository offers a series of Python scripts and programs to facilitate the process of automatic text text alignment using Hunalign or SBERT. To align the text files, they should be segmented. You can use [MTUOC-segmenter](https://github.com/aoliverg/MTUOC-segmenter), or any other program to segment the files prior aligning them. If you plan to use Hunalign, don't forget to add the paragraph mark (\<p\>). When segmenting the files. When using SBERT don't add the paragraph mark (\<p\>).

Before starting the alignment procedure, organize the files in the following way.

* Put all the source language segmented files in one directory (por example text-eng). 
* Put all the tarfet language segmented files in one directory (por example text-spa).

The source and target files should have the same name for both languages (for example, the source files: fileA.txt, file-B.txt, file_C.txt and the corresponding target files with exactly the same name, fileA.txt, file-B.txt, file_C.txt) or alternativelly, with a language code attached to the name  fileA-eng.txt, file-B-eng.txt, file_C-eng.txt and fileA-spa.txt, file-B-spa.txt, file_C-spa.txt).

Once you have organized the files in such way, you can start the alignment procedure.

## 1. Alignment with Hunalign

The programs MTUOC-aligner-hunalig.py (for the use in command line) and MTUOC-aligner-hunalign_GUI.py (with a Graphical User Interface, that is also provided as a Windows executable, MTUOC-aligner-hunalign_GUI.exe).

The compiled versions of hunalign for Linux (hunalign), Windows (hunalign.exe) and Mac (hunalignMAC) are provided. if you're using MAC rename hunalignMAC to hunalign. 

### 1.1. Bilingual dictionaries for alignment with Hunalign

To help to align we can use a bilingual dictionary. The bilingual dictionaries to use should be in the Hunalign format, that is: target_language_word @ source_language_word. For example, the English-Catalan dictionary would include the followint entries:

```
sionisme @ Zionism
abacà @ abaca
àbac @ abacus
abampere @ abampere
abandó @ abandonment
abandonament @ abandonment
reducció @ abatement
abadia @ abbey
...
```

You can download some alignment dictionaries created from the transfer dictionaries of the Apertium machine translation system from: [https://github.com/aoliverg/hunapertium](https://github.com/aoliverg/hunapertium). 

For other languages you can convert the bilingual dictionaries from the project [MUSE](https://github.com/facebookresearch/MUSE#ground-truth-bilingual-dictionaries) with the provided script MUSE2Hunalign.py. For example to create the English-Turkish dictionary download the full version of the [MUSE's English-Trukish dictionary](https://dl.fbaipublicfiles.com/arrival/dictionaries/en-tr.txt) and run:

```
python3 MUSE2Hunalign.py en-tr.txt alidict-en-tr.txt
```

The alidict-en-tr.txt file is the alignment dictionary in the required format.

The use of bilingual dictionaries is not compulsory, you can indicate an empty file (null.dic).


### 1.2. Alignment with Hunalign using the command line

To prepare the aligment script we use the program MTUOC-aligner-hunalign.py. To see the parameters use the -h option:

```python3 MTUOC-aligner-hunalign.py -h 

usage: MTUOC-aligner-hunalign.py [-h] --dirSL DIRSL --dirTL DIRTL --dirALI DIRALI --dictionary DICTIONARY --script
                                 SCRIPT [--r1 R1] [--r2 R2] [--windows]

A script to create the align script to be used with hunalign.

optional arguments:
  -h, --help            show this help message and exit
  --dirSL DIRSL         The input dir containing the segmented text files for the source language.
  --dirTL DIRTL         The input dir containing the segmented text files for the target language.
  --dirALI DIRALI       The output dir to save the aligned files.
  --dictionary DICTIONARY
                        The bilingual dictionary to use.
  --script SCRIPT       The name of the alignment script.
  --r1 R1               The first string for name replacement.
  --r2 R2               The second string for name replacement.
  --windows             Create a bat file for Windows.
```

Following the name of the directories in the examples above we can write:

```
python3 MTUOC-aligner-hunalign.py --dirSL text-eng --dirTL text-cat --dirALI alignments-eng-cat --dictionary hunapertium-en-ca.dic --script alignscript.sh --r1 eng.txt --r2 cat.txt
```

Further explanation of r1 and r2 paramenters should be given. These parameters indicates the endings of the file names that you should substract to make the source and target language file names equal. For example, if you have fileA-eng.txt and fileA-cat.txt you should indicate r1=-eng.txt and r2=-cat.txt to convert both names to fileA. **BUT** in this parameters you can not include hyphens (-), so you should indicate **--r1 eng.txt** and **--r2 cat.txt**.

And a script with the alignment instructions will be created, containing several lines as the following:

```
timeout 5m ./hunalign hunapertium-en-ca.dic -utf -realign -text "text-eng/fileA-eng.txt" "text-cat/fileA-cat.txt" > "alignments-eng-cat/ali-fileA-eng.txt"
```

To run the alignment process, give execution permisions to this script and to hunalign:

```
chmod +x alignscript.sh
chmod +x hunalign
```

Then run the script:

```
./alignscript.sh
```

And the alignment process will start. Once finished the alignment, select the alignments based on the confidence score as explained in section *3. Selecting the alignments*.

If you're working on Windows, dont forget to use the option --windows and use a .bat extension for the script file. The created instructions will be slightly different:

```
hunalign.exe hunapertium-en-ca.dic -utf -realign -text t "text-eng/fileA-eng.txt" "text-cat/fileA-cat.txt" > "alignments-eng-cat/ali-fileA-eng.txt"
```

Then you can run the bat file (either in the terminal or double-clicking on it.

### 1.2. Alignment with Hunalign using GUI version

The GUI version offers an intuitive interface to perform the same process. Remember that this version is distributed both as Python script and as a Windows executable file. Once you run the program, the following interface will appear:

![](https://github.com/aoliverg/imageswiki/blob/main/MTUOC-aligner-hunalign_GUI.PNG)

Simply fill all the required information and press the button **Create script!**.

Further explanation of Source lang. ending and Target lang. ending fields should be given. These parameters indicates the endings of the file names that you should substract to make the source and target language file names equal. For example, if you have fileA-eng.txt and fileA-cat.txt you should indicate -eng.txt and -cat.txt to convert both names to fileA. **BUT** in this parameters you can not include hyphens (-), so you should indicate **eng.txt** and **cat.txt**.

To run the alignment process, give execution permisions to this script and to hunalign:

```
chmod +x alignscript.sh
chmod +x hunalign
```

Then run the script:

```
./alignscript.sh
```

And the alignment process will start. Once finished the alignment, select the alignments based on the confidence score as explained in section *3. Selecting the alignments*.

If you're working on Windows, dont forget to use the mark option windows and use a .bat extension for the script file. Then you can run the bat file (either in the terminal or double-clicking on it.

## 2. Alignment with SBERT

The alignment using [SBERT](https://www.sbert.net/) allow both the aligment of parallel document and the process of finding parallel segments in comparable documents, that is, documents that are not translations of each other but talk about a similar topic. This process is also very useful when aligning parallel documents that differ in some sections of the document.

To align documents using SBERT you'll need the following programs:

* MTUOC-aligner-SBERT.py (running in the command line) or MTUOC-aligner-SBERT_GUI.py (with a graphical user inferface). The GUI version is also available as a Windows executable (MTUOC-aligner-SBERT_GUI.exe).
* MTUOC-bitext-mining.py: for the moment this script is only available as a Python v.3 script. Refer to the following requirements to run the script.

**Requirements to run MTUOC-bitext-mining.py**

This script is needed to run the alignment script created by MTUOC-aligner-SBERT. A Python v3 interpreter is needed. If you don't have one installed in your system you can download one from [www.python.org](www.python.org). Download the latest version 3 available for your operating system.

Then, you can install the following dependences using pip:

* faiss
* faiss_cpu or faiss_gpu if you have access to GPU units
* numpy
* scikit_learn
* sentence_transformers
* torch
* tqdm

### 2.1. Alignment with SBERT using the command line

We can get the instructions for using the MTUOC-aligner-SBERT.py using the -h option:

```
python3 MTUOC-aligner-SBERT.py -h
usage: MTUOC-aligner-SBERT.py [-h] --dirSL DIRSL --dirTL DIRTL --dirALI DIRALI --script SCRIPT [--r1 R1] [--r2 R2]

A script to create the align script to be used with SBERT.

optional arguments:
  -h, --help       show this help message and exit
  --dirSL DIRSL    The input dir containing the segmented text files for the source language.
  --dirTL DIRTL    The input dir containing the segmented text files for the target language.
  --dirALI DIRALI  The output dir to save the aligned files.
  --script SCRIPT  The name of the alignment script.
  --r1 R1          The first string for name replacement.
  --r2 R2          The second string for name replacement.
```

```
python3 MTUOC-aligner-SBERT.py --dirSL text-eng --dirTL text-cat --dirALI alignments-eng-cat --script alignscript.sh --r1 eng.txt --r2 cat.txt
```

Further explanation of r1 and r2 paramenters should be given. These parameters indicates the endings of the file names that you should substract to make the source and target language file names equal. For example, if you have fileA-eng.txt and fileA-cat.txt you should indicate r1=-eng.txt and r2=-cat.txt to convert both names to fileA. **BUT** in this parameters you can not include hyphens (-), so you should indicate **--r1 eng.txt** and **--r2 cat.txt**.

If you're working on Windows give a **.bat** extension to the alignment script. Once created the alignment script you can run it from the command line or double-clicking on it from the File Explorer.

If you're working on Linux or Mac, don't forget to give execution permissions to the script before running it:

```
chmod +x alignscript.sh
```

Once finished the alignment, select the alignments based on the confidence score as explained in section *3. Selecting the alignments*.

### 1.2. Alignment with SBERT using GUI version

The GUI version offers an intuitive interface to perform the same process. Remember that this version is distributed both as Python script and as a Windows executable file. Once you run the program, the following interface will appear:

![]([https://github.com/aoliverg/imageswiki/blob/main/MTUOC-aligner-SBERT_GUI.PNG](https://github.com/aoliverg/imageswiki/blob/main/MTUOC-aligner-SBERT_GUI.PNG))

Simply fill all the required information and press the button **Create script!**.

Further explanation of Source lang. ending and Target lang. ending fields should be given. These parameters indicates the endings of the file names that you should substract to make the source and target language file names equal. For example, if you have fileA-eng.txt and fileA-cat.txt you should indicate -eng.txt and -cat.txt to convert both names to fileA. **BUT** in this parameters you can not include hyphens (-), so you should indicate **eng.txt** and **cat.txt**.

If you're working on Windows give a **.bat** extension to the alignment script. Once created the alignment script you can run it from the command line or double-clicking on it from the File Explorer.

If you're working on Linux or Mac, don't forget to give execution permissions to the script before running it:

```
chmod +x alignscript.sh
```

Once finished the alignment, select the alignments based on the confidence score as explained in section *3. Selecting the alignments*.

## 3. Selecting the alignments

The result of an alignment process, both with Hunalign or woth SBERT, is a directory containing a set of files with lines containing the source segment, the target segment and a confidence score, separated by tabulators. For example:

```
A man is suspected of a crime months perhaps after it has been committed.	De vegades es sospita que un home és l'autor d'un crim mesos després que s'hagi comès.	1.7361
```

Now we are interested in selecting all the segments with a higher confidence than a given one. To set this confidence, a visual exploration of several alignment files is advisable. To do so we can unse the program selectAlignments.py. If you use the option -h you'll get the information on how to use it:

```
python3 selectAlignments.py -h
usage: selectAlignments.py [-h] -i INDIR -o OUTFILE -c CONFIDENCE

A script to select aligments in a directory with a higher confidence than the given one into a single file. The
alignment file should be a TSV file with three fields: source segment, target segment, confidence score.

optional arguments:
  -h, --help            show this help message and exit
  -i INDIR, --inDir INDIR
                        The input dir containing the hunalign alignments.
  -o OUTFILE, --outFile OUTFILE
                        The input fule.
  -c CONFIDENCE, --confidence CONFIDENCE
                        The minimun confidence (the output confidence will be highet tnar the one provided..
```

For example, the command:

```
python3 selectAlignments.py -i alignments-eng-cat -o selectedalignments.txt -c 0
```

will create the file selectedalignments.tx containing all the segment pairs with a confidence higher than 0 from the directory alignments-eng-cat.

This program is also distributed with a Graphical User Inferface (selectAlignments_GUI.py) and as a Windows executable (selectAlignments_GUI.exe). Once started the program, the following interface will appear:

![](https://github.com/aoliverg/imageswiki/blob/main/selectAlignments_GUI.PNG)

Fill all the information and press the button **Go!**.
