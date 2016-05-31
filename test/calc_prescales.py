#!/usr/bin/env python
import ROOT

t = ROOT.TChain("trigAna/TrigTree")

t.Add( "SMPJ_TriggerAna/crab_jetht2015B/results/TriggerAna_data_*.root" )

trigmap = {
    'HLT_PFJet40',
    'HLT_PFJet80',
    'HLT_PFJet140',
    'HLT_PFJet200',
    'HLT_PFJet260',
    'HLT_PFJet320',
    'HLT_PFJet400',
    'HLT_PFJet450',
    'HLT_PFJet500',
    }

counts = dict( zip( trigmap, [0] * len(trigmap) ) )
prescales = dict( zip( trigmap, [0] * len(trigmap) ) )


trigentries = ROOT.TH1F("trigentries", ';Trigger;Number', len(trigmap), 0, len(trigmap) )

nentries = t.GetEntries()
#for ientry in xrange(0, nentries ) :
for ientry in xrange(0, 1000 ) :
    t.GetEntry(ientry)

    if ientry % 10000 == 0 :
        print '%12d / %12d' % (ientry, nentries )
    for itrig in xrange(0, len(t.Fired)):
        if t.Fired[itrig] > 0 :
            name = t.triggerList[itrig].split( "_v" )[0]
            counts[ name ] += 1
            prescales[name] += t.L1Prescales[itrig] * t.HLTPrescales[itrig]
            trigentries.Fill( itrig, t.L1Prescales[itrig] * t.HLTPrescales[itrig] )
            #print '%30s : %3d %10d %10d' % ( t.triggerList[itrig], t.Fired[itrig], t.L1Prescales[itrig], t.HLTPrescales[itrig]) 


for trig in trigmap :
    if counts[trig] > 0 : 
        print '%30s : %12d %12.2f' % ( trig, counts[trig], float(prescales[trig]) / counts[trig] )


c1 = ROOT.TCanvas("c1", "c1")
trigentries.Draw()
