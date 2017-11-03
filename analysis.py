__author__ = 'lello'

import csv
import sys
import math

# IMPORTANT: The input file must be sorted with the Student ID.

filename = sys.argv[1]
IDList = []
CFUList=[]
ExamIDList=[]
CourseList = []
FullStudentList = []

ID_col = 9 
EXAMID_col = 14
CFU_col = 16
Course_col = 2
Passed_col = 22

with open(filename,'rt',encoding="utf8") as f:
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
                ExamIDList.append(str(row[EXAMID_col]).strip())
                CourseList.append(str(row[Course_col]).strip())

# Some statistics
StudentSet = set(tuple(x) for x in FullStudentList)
print("Student number: ", len(StudentSet))
ExamID = ['001702', '001703', '001717', '001711']
c = [0, 0, 0, 0]
for k in range(len(c)):
    for s in StudentSet:
        c[k] += s.count(ExamID[k])
for i in range(len(c)):
    print(ExamID[i], " students: ", c[i])

# Processing data
ExamSet_SFA = set([ 'AGR0048', 'AGR0004', 'AGR0007', 'AGR0047', 'SAF0050', 'AGR0051', 'AGR0008', 'AGR0059', 'AGR0020'])
ExamSet_STA = set([ 'AGR0048', 'AGR0004', 'AGR0007', 'AGR0047', 'SAF0050', 'AGR0051', 'AGR0008', 'AGR0055', 'AGR0025'])
ExamSet_TAL = set([ 'AGR0395', 'AGR0027', 'AGR0025', 'AGR0011', 'SAF0050', 'AGR0017', 'AGR0016', 'AGR0012', 'AGR0045', 'AGR0295'])
ExamSet_VE = set([ 'AGR0395', 'AGR0027', 'AGR0025', 'AGR0138', 'AGR0011', 'SAF0050', 'AGR0017', 'AGR0016', 'AGR0012', 'AGR0331', 'AGR0295'])

ExamSet = dict([('001702', ExamSet_VE) ,('001703', ExamSet_TAL), ('001717', ExamSet_STA), ('001711', ExamSet_SFA) ])

FinalList = []
CDSFinalList = dict([('001702', []),('001703',[]),('001717',[]),('001711',[])])

i0 = -1
for i in range(len(IDList)-1):
    #print(IDList[i+1], "  ",  IDList[i])
    if (IDList[i+1] == IDList[i]): 
        if (i0 == -1): 
            i0 = i
    else:
        i1 = i
        if (i0 == -1):
            i0 = i1
        s = 0
        for k in range(i0,i1+1):
            #print(IDList[k], ExamIDList[k], len(ExamIDList[k]))
            if ExamIDList[k] in ExamSet[CourseList[k]]:
                #print(IDList[k], ExamIDList[k], CFUList[k])
                s += CFUList[k]
        CDSFinalList[CourseList[i]].append([IDList[i], s])
        #s =  sum(CFUList[i0:i1+1])
        FinalList.append([IDList[i], s])
        #print(IDList[i], s, i0, i1)
        #print(IDList[i], s)
        i0 = -1

FinalList.sort(key=lambda x: x[1], reverse=True)

#print("matricola;voto;voto-no-open;mcq;numeric;open;esame")
for l in FinalList:
    #res = '%d; %d; %.2f; %.2f; %.2f; %.2f; %d' % (l[1], l[2], l[3], l[4], l[5], l[6], l[0])
    res = '%d; %d ' % (l[0], l[1])
#    print(res)

for k in ['001702', '001703', '001717', '001711']:
    CDSFinalList[k].sort(key=lambda x: x[1], reverse=True)
    for l in CDSFinalList[k]:
        #res = '%d; %d; %.2f; %.2f; %.2f; %.2f; %d' % (l[1], l[2], l[3], l[4], l[5], l[6], l[0])
        res = '%s; %d; %d ' % (k, l[0], l[1])
        print(res)
