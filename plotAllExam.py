import ROOT as r
import os

author = "__pmo__"

r.gROOT.SetBatch(True)

f=r.TFile("ExamHistograms.root")

CDSlist=['001717','001702','001711','001703']

exams=dict()
exams['001717'] = ['AGR0048', 'AGR0004', 'AGR0007', 'AGR0047', 'AGR0051', 'AGR0008', 'AGR0055']
exams['001702'] = ['AGR0395', 'AGR0027', 'AGR0011', 'AGR0017', 'AGR0016', 'AGR0012', 'AGR0331']
exams['001711'] = ['AGR0048', 'AGR0004', 'AGR0007', 'AGR0047', 'AGR0051', 'AGR0008', 'AGR0059'] 
exams['001703'] = ['AGR0395', 'AGR0027', 'AGR0011', 'AGR0017', 'AGR0016', 'AGR0012', 'AGR0045']

c1=r.TCanvas("c1","c1",900,600)
#r.SetStyle("Plain")

#create destination subfolders for cds
for cds in CDSlist:
    os.system("mkdir -p %s"%(cds))

for cds in CDSlist:
    for exam in exams[cds]:
        print "%s_%s"%(exam,exams[cds].index(exam)+1) 
        a=f.Get("%s_%s"%(exam,cds))
        if a.GetMean()>0:
            a.GetXaxis().SetTitle("Voto %s"%exam)
            a.Rebin(2)
            a.Draw()
            c1.SaveAs("%s/%s-%s.png"%(cds,exam,cds))

corr_plot=dict()
for cds in CDSlist:
    corr_plot[cds]=r.TH2F("corr_%s"%cds,"corr_%s"%cds,len(exams[cds]),0.5,len(exams[cds])+0.5,len(exams[cds]),0.5,len(exams[cds])+0.5)
    for ex in exams[cds]:
        corr_plot[cds].GetXaxis().SetBinLabel(exams[cds].index(ex)+1,ex)
        corr_plot[cds].GetYaxis().SetBinLabel(exams[cds].index(ex)+1,ex)

for cds in CDSlist:
    for ex in exams[cds]:
        for ex1 in exams[cds]:
            a=f.Get("(%s,%s)_%s"%(ex,ex1,cds))
            if a.GetMean()>0:
#                a.Rebin(2)
                a.Draw("COLZ")
                corr_plot[cds].SetBinContent(exams[cds].index(ex)+1,exams[cds].index(ex1)+1,a.GetCorrelationFactor())
                c1.SaveAs("%s/%s_vs_%s-%s.png"%(cds,ex,ex1,cds))

r.gStyle.SetPalette(56)
            
for cds in CDSlist:
    corr_plot[cds].SetStats(0)
    corr_plot[cds].Draw("COLZ")
    c1.SaveAs("%s/corr_%s.png"%(cds,cds))

for cds in CDSlist:
    print "=========== %s =========="%(cds)
    for exam in exams[cds]:
        print "%s => %s"%(exam,exams[cds].index(exam)+1) 

    for ex in range(0,len(exams[cds])-1):
        for ex1 in range(ex+1,len(exams[cds])):
            a=f.Get("(%s,%s)_%s"%(exams[cds][ex],exams[cds][ex1],cds))
            print "%s vs %s: %3.2f"%(exams[cds][ex],exams[cds][ex1],a.GetCorrelationFactor())


