#!/usr/bin/env python

##########################################################
# hmmsearch parser for the dbCAN database.
#
# Based off the hmmscan parser used in the dbCAN server,
# written by Tanner Yohe under the supervision
# of Dr. Yin in the YinLab at NIU.
#
# Written by Antonio P. Camargo.
#
# INPUTS:
# python hmmsearch-parser-dbCAN.py <hmmsearch_domtblout> [eval] [coverage]
# eval and coverage are optional, hmmsearch_domtblout is required.
#
###########################################################

from subprocess import call
import sys

# Default thresholds:
eval = 1e-15
coverage = 0.35

if len(sys.argv) > 1:
    inputFile = sys.argv[1]
else:
    print("Please give a hmmsearch domtblout file as the first command")
    exit()

if len(sys.argv) > 3:
    eval = float(sys.argv[2])
    coverage = float(sys.argv[3])

call("cat "+inputFile+" | grep -v '^#' | awk '{print $1,$3,$4,$6,$13,$16,$17,$18,$19}' | sed 's/ /\t/g' | sort -k 3,3 -k 8n -k 9n | perl -e 'while(<>){chomp;@a=split;next if $a[-1]==$a[-2];push(@{$b{$a[2]}},$_);}foreach(sort keys %b){@a=@{$b{$_}};for($i=0;$i<$#a;$i++){@b=split(/\t/,$a[$i]);@c=split(/\t/,$a[$i+1]);$len1=$b[-1]-$b[-2];$len2=$c[-1]-$c[-2];$len3=$b[-1]-$c[-2];if($len3>0 and ($len3/$len1>0.5 or $len3/$len2>0.5)){if($b[4]<$c[4]){splice(@a,$i+1,1);}else{splice(@a,$i,1);}$i=$i-1;}}foreach(@a){print $_.\"\n\";}}' > temp", shell=True)
call("cat "+inputFile+" | grep -v '^#' | awk '{print $4,$6,$1,$3,$13,$16,$17,$18,$19}' | sed 's/ /\t/g' | sort -k 3,3 -k 8n -k 9n | perl -e 'while(<>){chomp;@a=split;next if $a[-1]==$a[-2];push(@{$b{$a[2]}},$_);}foreach(sort keys %b){@a=@{$b{$_}};for($i=0;$i<$#a;$i++){@b=split(/\t/,$a[$i]);@c=split(/\t/,$a[$i+1]);$len1=$b[-1]-$b[-2];$len2=$c[-1]-$c[-2];$len3=$b[-1]-$c[-2];if($len3>0 and ($len3/$len1>0.5 or $len3/$len2>0.5)){if($b[4]<$c[4]){splice(@a,$i+1,1);}else{splice(@a,$i,1);}$i=$i-1;}}foreach(@a){print $_.\"\n\";}}' > temp", shell=True)

print('Family_HMM\tHMM_length\tQuery_ID\tQuery_length\tE-value\tHMM_start\tHMM_end\tQuery_start\tQuery_end\tCoverage')
with open('temp') as f:
    for line in f:
        row = line.rstrip().split('\t')
        row[0] = row[0].replace('.hmm', '')
        row.append(float(int(row[6])-int(row[5]))/int(row[1]))
        if float(row[4]) <= eval and float(row[-1]) >= coverage:
            print('\t'.join([str(x) for x in row]))

call(['rm', 'temp'])
