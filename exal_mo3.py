#!/usr/bin/env python

###########################################################################
#
# Calcola quanti hanno superato l'esame per insegnamento
#
###########################################################################

__author__ = 'lello'

import csv
import sys
import math
import numpy as np

# IMPORTANT: The input file must be sorted with the Student ID.

filename = sys.argv[1]
YEAR = sys.argv[2]
EXAM = sys.argv[3]
IDList = []
CFUList=[]
ScoreList=[]
ExamIDList=[]
CourseList = []
DateList = []
FullStudentList = []

ID_col = 9 
EXAMID_col = 14
CFU_col = 16
Score_col = 17
Course_col = 2
Date_col = 20
Passed_col = 22

#with open(filename,'rt',encoding="utf8") as f:
with open(filename,'rt') as f: 
    #mycsv = csv.reader(f,delimiter=';',quoting=csv.QUOTE_NONNUMERIC)
    mycsv = csv.reader(f,delimiter=',')
    origcsv = list(mycsv)
    mycsv = sorted(origcsv, key=lambda row: row[ID_col], reverse=True) 
    # del mycsv[0] # remove headers
    for row in mycsv:
        try:
            studentID = int(row[ID_col])
            studentFound = True
        except ValueError:
            studentFound = False
        if (studentFound):
            FullStudentList.append([studentID, str(row[Course_col]).strip()])
            if (str(row[Passed_col]).strip() == "Sostenuto"):
                #print(row)
                IDList.append(int(row[ID_col]))
                CFUList.append(int(row[CFU_col]))
                if row[Score_col] == "":
                    row[Score_col] = 0
                #print(row[Score_col])
                ScoreList.append(int(row[Score_col]))
                ExamIDList.append(str(row[EXAMID_col]).strip())
                DateList.append(str(row[Date_col]).strip()[-4:])
                CourseList.append(str(row[Course_col]).strip())

# Some statistics
StudentSet = set(tuple(x) for x in FullStudentList)
print("Student number: ", len(StudentSet))
CDSID = ['001702', '001703', '001717', '001711']
c = [0, 0, 0, 0]
for k in range(len(c)):
    for s in StudentSet:
        c[k] += s.count(CDSID[k])
#for i in range(len(c)):
#    print(CDSID[i], " students: ", c[i])

CDS_NStudents = {'001702': c[0], '001703' : c[1], '001717': c[2], '001711': c[3]}

# Processing data
ExamSet_SFA = set([ 'AGR0048', 'AGR0004', 'AGR0007', 'AGR0047', 'SAF0050', 'AGR0051', 'AGR0008', 'AGR0059', 'AGR0020'])
ExamSet_STA = set([ 'AGR0048', 'AGR0004', 'AGR0007', 'AGR0047', 'SAF0050', 'AGR0051', 'AGR0008', 'AGR0055', 'AGR0025'])
ExamSet_TAL = set([ 'AGR0395', 'AGR0027', 'AGR0025', 'AGR0011', 'SAF0050', 'AGR0017', 'AGR0016', 'AGR0012', 'AGR0045', 'AGR0295'])
ExamSet_VE = set([ 'AGR0395', 'AGR0027', 'AGR0025', 'AGR0138', 'AGR0011', 'SAF0050', 'AGR0017', 'AGR0016', 'AGR0012', 'AGR0331', 'AGR0295'])

ControlSet = set([EXAM])
#ControlSet = set(['AGR0138'])
#ControlSet2 = set(['AGR0140'])
ExamSet = dict([('001702', ExamSet_VE.intersection(ControlSet)) ,
                ('001703', ExamSet_TAL.intersection(ControlSet)), 
                ('001717', ExamSet_STA.intersection(ControlSet)), 
                ('001711', ExamSet_SFA.intersection(ControlSet)) ])

FinalList = []
CDSFinalList = dict([('001702', []),('001703',[]),('001717',[]),('001711',[])])

score = 0
i0 = -1
#MO i loop over the students 
for i in range(len(IDList)-1):
    #print(" ID ",  IDList[i])
    if (IDList[i+1] == IDList[i]): 
        #Pick i-th student
        if (i0 == -1):
            i0 = i
    else:
        i1 = i
        if (i0 == -1):
            i0 = i1
        s = 0
#MO score initialized        
        score=0
        #MO k runs over the exames
        for k in range(i0,i1+1):
            #print(IDList[k], ExamIDList[k], len(ExamIDList[k]))
            if ExamIDList[k] in ExamSet[CourseList[k]] and DateList[k] <= YEAR:
                #print(IDList[k], ExamIDList[k], CFUList[k])
                s += CFUList[k]
# MO Add score and eliminate print for VE
                score = ScoreList[k]
                #if CourseList[i] == "001702":
                #    score = ScoreList[k]
                #    print(score, CourseList[i])
# MO add score in CDSFinalList 
        CDSFinalList[CourseList[i]].append([IDList[i], s, score])
        #s =  sum(CFUList[i0:i1+1])
        FinalList.append([IDList[i], s])
        #print(IDList[i], s, i0, i1)
        #print(IDList[i], s)
        # reset counter
        i0 = -1

# Sort list over CFU
FinalList.sort(key=lambda x: x[1], reverse=True)

#print("matricola;voto;voto-no-open;mcq;numeric;open;esame")
#for l in FinalList:
    #res = '%d; %d; %.2f; %.2f; %.2f; %.2f; %d' % (l[1], l[2], l[3], l[4], l[5], l[6], l[0])
#    res = '%d; %d ' % (l[0], l[1])
#    print(res)

for k in ['001702', '001703', '001717', '001711']:
    CDSFinalList[k].sort(key=lambda x: x[1], reverse=True)
    exl = [row[1] for row in CDSFinalList[k]] 
#MO Add score    
    exlscore = [row[2] for row in CDSFinalList[k]]
    # Numer of students that have passed the exam
    sxl = (np.asarray(exl) > 0).sum()
#MO Add average score
    if (sxl > 0):
        avg_score = float(np.asarray(exlscore).sum())/sxl
    else:
        avg_score = 0.
    res = '%s %s %s %d %d %.1f %.1f' % (k, EXAM, YEAR, sxl, CDS_NStudents[k], float(sxl)/CDS_NStudents[k]*100, avg_score)
    #res = '%s: %d / %d; %.1f' % (k, sxl, CDS_NStudents[k], sxl/CDS_NStudents[k]*100)
    print(res)
    #for l in CDSFinalList[k]:
    #    res = '%s; %d; %d ' % (k, l[0], l[1])
    #    print(res)

