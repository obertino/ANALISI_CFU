import ROOT as r

r.gROOT.SetBatch(True)

f=r.TFile("ExamHistograms.root")

CDSlist=['001717']
exams = ['AGR0048', 'AGR0004', 'AGR0007', 'AGR0047', 'AGR0051', 'AGR0008', 'AGR0055']

c1=r.TCanvas("c1","c1",900,600)
#r.SetStyle("Plain")

for exam in exams:
    for cds in CDSlist:
        print "%s_%s"%(exam,exams.index(exam)+1) 
        a=f.Get("%s_%s"%(exam,cds))
        if a.GetMean()>0:
            a.GetXaxis().SetTitle("Voto %s"%exam)
            a.Rebin(2)
            a.Draw()
            c1.SaveAs("%s-%s.png"%(exam,cds))

corr_plot=dict()
for cds in CDSlist:
    corr_plot[cds]=r.TH2F("corr_%s"%cds,"corr_%s"%cds,len(exams),0.5,len(exams)+0.5,len(exams),0.5,len(exams)+0.5)
    for ex in exams:
        corr_plot[cds].GetXaxis().SetBinLabel(exams.index(ex)+1,ex)
        corr_plot[cds].GetYaxis().SetBinLabel(exams.index(ex)+1,ex)

for ex in exams:
    for ex1 in exams:
        for cds in CDSlist:
            a=f.Get("(%s,%s)_%s"%(ex,ex1,cds))
            if a.GetMean()>0:
#                a.Rebin(2)
                a.Draw("COLZ")
                corr_plot[cds].SetBinContent(exams.index(ex)+1,exams.index(ex1)+1,a.GetCorrelationFactor())
                c1.SaveAs("%s_vs_%s-%s.png"%(ex,ex1,cds))

r.gStyle.SetPalette(56)
            
for cds in CDSlist:
    corr_plot[cds].SetStats(0)
    corr_plot[cds].Draw("COLZ")
    c1.SaveAs("corr_%s.png"%(cds))

for exam in exams:
    print "%s => %s"%(exam,exams.index(exam)+1) 


for ex in range(0,len(exams)-1):
    for ex1 in range(ex+1,len(exams)):
        for cds in CDSlist:
            a=f.Get("(%s,%s)_%s"%(exams[ex],exams[ex1],cds))
            print "%s vs %s: %3.2f"%(exams[ex],exams[ex1],a.GetCorrelationFactor())
