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
import ROOT as r

# IMPORTANT: The input file must be sorted with the Student ID.

filename = sys.argv[1]
YEAR = sys.argv[2]
#EXAM = sys.argv[3]
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
#print("Student number: ", len(StudentSet))
CDSID = ['001702', '001703', '001717', '001711']
c = [0, 0, 0, 0]
for k in range(len(c)):
    for s in StudentSet:
        c[k] += s.count(CDSID[k])
for i in range(len(c)):
    print(CDSID[i], " students: ", c[i])

CDS_NStudents = {'001702': c[0], '001703' : c[1], '001717': c[2], '001711': c[3]}

# Processing data
ExamSet_SFA = set([ 'AGR0048', 'AGR0004', 'AGR0007', 'AGR0047', 'SAF0050', 'AGR0051', 'AGR0008', 'AGR0059', 'AGR0020'])
ExamSet_STA = set([ 'AGR0048', 'AGR0004', 'AGR0007', 'AGR0047', 'SAF0050', 'AGR0051', 'AGR0008', 'AGR0055', 'AGR0025'])
ExamSet_TAL = set([ 'AGR0395', 'AGR0027', 'AGR0025', 'AGR0011', 'SAF0050', 'AGR0017', 'AGR0016', 'AGR0012', 'AGR0045', 'AGR0295'])
ExamSet_VE = set([ 'AGR0395', 'AGR0027', 'AGR0025', 'AGR0138', 'AGR0011', 'SAF0050', 'AGR0017', 'AGR0016', 'AGR0012', 'AGR0331', 'AGR0295'])

#ControlSet = set([EXAM])
#ControlSet = set(['AGR0138'])
#ControlSet2 = set(['AGR0140'])
#ExamSet = dict([('001702', ExamSet_VE.intersection(ControlSet)) ,
#                ('001703', ExamSet_TAL.intersection(ControlSet)), 
#                ('001717', ExamSet_STA.intersection(ControlSet)), 
#                ('001711', ExamSet_SFA.intersection(ControlSet)) ])
ExamSet = dict([('001702', ExamSet_VE) ,
                ('001703', ExamSet_TAL), 
                ('001717', ExamSet_STA), 
                ('001711', ExamSet_SFA) ])

FinalList = []
CDSFinalList = dict([('001702', []),('001703',[]),('001717',[]),('001711',[])])

score = 0
i0 = -1

#i loop over the students 
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

        #k runs over the exames
        exams=dict()
        for ex in ExamSet[CourseList[i]]:
            s=0
            score=0
            for k in range(i0,i1+1):
            #print(IDList[k], ExamIDList[k], len(ExamIDList[k]))
                if ExamIDList[k] == ex and DateList[k] <= YEAR:
                #print(IDList[k], ExamIDList[k], CFUList[k])
                    s = CFUList[k]
                    score = ScoreList[k]
                #                if CourseList[i] == "001702":
                #                    score = ScoreList[k]
                    #print(score, CourseList[i])
                    #       CDSFinalList[CourseList[i]].append([IDList[i], s])
                exams[ex]=[s,score]
        CDSFinalList[CourseList[i]].append([IDList[i], exams])
        #s =  sum(CFUList[i0:i1+1])
        FinalList.append([IDList[i], exams])
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

#print CDSFinalList

f=r.TFile("ExamHistograms.root","RECREATE")


for k in ['001702', '001703', '001717', '001711']:
    print "============= %s ================"%k
    students=r.TH1F("NStudents_%s"%k,"NStudents_%s"%k,2,-0.5,1.5)
    exams=dict()
    exams_corr=dict()
    for ex in ExamSet[k]:
        exams[ex]=r.TH1F("%s_%s"%(ex,k),"%s_%s"%(ex,k),14,17.5,31.5)
        exams[ex].GetXaxis().SetTitle(ex)
    for ex in ExamSet[k]:
        for ex1 in ExamSet[k]:
            exams_corr["(%s,%s)"%(ex,ex1)]=r.TH2F("(%s,%s)_%s"%(ex,ex1,k),"(%s,%s)_%s"%(ex,ex1,k),14,17.5,31.5,14,17.5,31.5)
            exams_corr["(%s,%s)"%(ex,ex1)].GetXaxis().SetTitle(ex)
            exams_corr["(%s,%s)"%(ex,ex1)].GetYaxis().SetTitle(ex1)
    for s_exams in CDSFinalList[k]:
        students.Fill(1)
        ex_list=s_exams[1]
        for ex in ex_list.keys():
#            print "%s: %s => (%s,%s)"%(s_exams[0],ex, ex_list[ex][0],ex_list[ex][1])
            if ex_list[ex][0]>0:
                exams[ex].Fill(ex_list[ex][1])
        for ex in ex_list.keys():
            for ex1 in ex_list.keys():
                if ex_list[ex][0]>0:
                    if ex_list[ex1][0]>0:
                        exams_corr["(%s,%s)"%(ex,ex1)].Fill(ex_list[ex][1],ex_list[ex1][1])
#CDSFinalList[k].sort(key=lambda x: x[1], reverse=True)
#    exl = [row[1] for row in CDSFinalList[k]] 
#    exlscore = [row[2] for row in CDSFinalList[k]]
#    for row in CDSFinalList[k]:
#        a.Fill(row[2])
#    # Number of students that have passed the exam
#    sxl = (np.asarray(exl) > 0).sum()
#    if (sxl > 0):
#        avg_score = float(np.asarray(exlscore).sum())/sxl
#    else:
#        avg_score = 0.
#    res = '%s %s %s %d %d %.1f %.1f' % (k, EXAM, YEAR, sxl, CDS_NStudents[k], float(sxl)/CDS_NStudents[k]*100, avg_score)
#    print(res)
    students.Write()
    students.Print()
    for ex in ExamSet[k]:
        exams[ex].Write()
        exams[ex].Print()
    for ex in ExamSet[k]:
        for ex1 in ExamSet[k]:
            exams_corr["(%s,%s)"%(ex,ex1)].Write()
            exams_corr["(%s,%s)"%(ex,ex1)].Print()
    #for l in CDSFinalList[k]:
    #    res = '%s; %d; %d ' % (k, l[0], l[1])
    #    print(res)
f.Write()
f.Close()
