import FWCore.ParameterSet.Config as cms

process = cms.Process("Ana")
process.load('FWCore.MessageService.MessageLogger_cfi')
##-------------------- Communicate with the DB -----------------------
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.GlobalTag.globaltag = 'FT_53_V21_AN6::All'
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.Geometry.GeometryIdeal_cff')
process.load('RecoJets.Configuration.RecoPFJets_cff')
process.load('RecoJets.Configuration.RecoJets_cff')
process.load('CommonTools/RecoAlgos/HBHENoiseFilterResultProducer_cfi')
##-------------------- Import the JEC services -----------------------
process.load('JetMETCorrections.Configuration.DefaultJEC_cff')
#-------- HCAL Laser Filter ------#
process.load("RecoMET.METFilters.hcalLaserEventFilter_cfi")
process.load('EventFilter.HcalRawToDigi.hcallasereventfilter2012_cfi')
#process.load('EventFilter.HcalRawToDigi.hcallaserhbhehffilter2012_cfi')
## The ECAL dead cell trigger primitive filter _______________________________||
process.load('RecoMET.METFilters.EcalDeadCellTriggerPrimitiveFilter_cfi')
## The EE bad SuperCrystal filter ____________________________________________||
process.load('RecoMET.METFilters.eeBadScFilter_cfi')
## TRACKING Filter 
process.load('RecoMET.METFilters.trackingFailureFilter_cfi')
## The ECAL laser correction filter
process.load('RecoMET.METFilters.ecalLaserCorrFilter_cfi')

#############   Set the number of events #############
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)
#############   Format MessageLogger #################
process.MessageLogger.cerr.FwkReport.reportEvery = 10000
#############   Define the source file ###############
process.source = cms.Source("PoolSource",
#    fileNames = cms.untracked.vstring('/store/data/Run2012C/JetHT/AOD/PromptReco-v2/000/198/941/221BEAC8-7ACF-E111-8A3D-E0CB4E4408E7.root')
   fileNames = cms.untracked.vstring(
'/store/data/Run2015B/JetHT/MINIAOD/PromptReco-v1/000/251/252/00000/263D331F-AF27-E511-969B-02163E012627.root',
'/store/data/Run2015B/JetHT/MINIAOD/PromptReco-v1/000/251/252/00000/52F74C29-AF27-E511-BAA1-02163E01358B.root',
'/store/data/Run2015B/JetHT/MINIAOD/PromptReco-v1/000/251/252/00000/583CFB34-AF27-E511-8639-02163E0135AC.root',
'/store/data/Run2015B/JetHT/MINIAOD/PromptReco-v1/000/251/252/00000/8A22C61F-AF27-E511-B6BF-02163E012620.root',
'/store/data/Run2015B/JetHT/MINIAOD/PromptReco-v1/000/251/252/00000/8C85BC1E-AF27-E511-9E2D-02163E012AA4.root',
'/store/data/Run2015B/JetHT/MINIAOD/PromptReco-v1/000/251/252/00000/9604D91E-AF27-E511-8C5A-02163E014166.root',
'/store/data/Run2015B/JetHT/MINIAOD/PromptReco-v1/000/251/252/00000/AA9FA822-AF27-E511-BCD7-02163E0133A4.root',
'/store/data/Run2015B/JetHT/MINIAOD/PromptReco-v1/000/251/252/00000/B28F4A1F-AF27-E511-8471-02163E0135C9.root',
'/store/data/Run2015B/JetHT/MINIAOD/PromptReco-v1/000/251/252/00000/B2B3821D-AF27-E511-A054-02163E01267F.root',
'/store/data/Run2015B/JetHT/MINIAOD/PromptReco-v1/000/251/252/00000/CCF39221-AF27-E511-82FB-02163E0142FD.root',
'/store/data/Run2015B/JetHT/MINIAOD/PromptReco-v1/000/251/252/00000/D231F61F-AF27-E511-97A9-02163E013432.root',
'/store/data/Run2015B/JetHT/MINIAOD/PromptReco-v1/000/251/252/00000/F8295A1B-AF27-E511-89C2-02163E014289.root',       
       )
)
############# processed tree producer ##################
process.TFileService = cms.Service("TFileService",fileName = cms.string('TriggerAna_data.root'))

process.trigAna = cms.EDAnalyzer('TriggerAnaPlugin',
    ## trigger ###################################
    printTriggerMenu = cms.untracked.bool(True),
    processName     = cms.string('HLT'),
    triggerName     = cms.vstring('HLT_PFJet40_v2', 'HLT_PFJet40_v3', 'HLT_PFJet40_v4','HLT_PFJet40_v5','HLT_PFJet40_v6','HLT_PFJet40_v7','HLT_PFJet40_v8','HLT_PFJet40_v9',
                                  'HLT_PFJet80_v2', 'HLT_PFJet80_v3', 'HLT_PFJet80_v4','HLT_PFJet80_v5','HLT_PFJet80_v6','HLT_PFJet80_v7','HLT_PFJet80_v8','HLT_PFJet80_v9',
                                  'HLT_PFJet140_v2','HLT_PFJet140_v3','HLT_PFJet140_v4','HLT_PFJet140_v5','HLT_PFJet140_v6','HLT_PFJet140_v7','HLT_PFJet140_v8','HLT_PFJet140_v9',
                                  'HLT_PFJet200_v2','HLT_PFJet200_v3','HLT_PFJet200_v4','HLT_PFJet200_v5','HLT_PFJet200_v6','HLT_PFJet200_v7','HLT_PFJet200_v8','HLT_PFJet200_v9',
                                  'HLT_PFJet260_v2','HLT_PFJet260_v3','HLT_PFJet260_v4','HLT_PFJet260_v5','HLT_PFJet260_v6','HLT_PFJet260_v7','HLT_PFJet260_v8','HLT_PFJet260_v9',
                                  'HLT_PFJet320_v2','HLT_PFJet320_v3','HLT_PFJet320_v4','HLT_PFJet320_v5','HLT_PFJet320_v6','HLT_PFJet320_v7','HLT_PFJet320_v8','HLT_PFJet320_v9',
                                  'HLT_PFJet400_v2','HLT_PFJet400_v3','HLT_PFJet400_v4','HLT_PFJet400_v5','HLT_PFJet400_v6','HLT_PFJet400_v7','HLT_PFJet400_v8','HLT_PFJet400_v9',
                                  'HLT_PFJet450_v2','HLT_PFJet450_v3','HLT_PFJet450_v4','HLT_PFJet450_v5','HLT_PFJet450_v6','HLT_PFJet450_v7','HLT_PFJet450_v8','HLT_PFJet450_v9',
                                  'HLT_PFJet500_v2','HLT_PFJet500_v3','HLT_PFJet500_v4','HLT_PFJet500_v5','HLT_PFJet500_v6','HLT_PFJet500_v7','HLT_PFJet500_v8','HLT_PFJet500_v9',
    ),
    triggerResults  = cms.InputTag("TriggerResults","","HLT")
)

############# hlt filter #########################
process.hltFilter = cms.EDFilter('HLTHighLevel',
    TriggerResultsTag  = cms.InputTag('TriggerResults','','HLT'),
    HLTPaths           = cms.vstring(
    'HLT_PFJet40_v*','HLT_PFJet80_v*','HLT_PFJet140_v*','HLT_PFJet200_v*','HLT_PFJet260_v*','HLT_PFJet320_v*','HLT_PFJet400_v*','HLT_PFJet450_v*','HLT_PFJet500_v*',
    ),
    eventSetupPathsKey = cms.string(''),
    andOr              = cms.bool(True), #----- True = OR, False = AND between the HLTPaths
    throw              = cms.bool(False)
)



process.path = cms.Path(process.hltFilter * process.HBHENoiseFilterResultProducer * process.hcalLaserEventFilter *
process.hcallasereventfilter2012 * #process.hcallaserhbhehffilter2012 *
process.EcalDeadCellTriggerPrimitiveFilter * #process.eeBadScFilter*
process.trigAna )

