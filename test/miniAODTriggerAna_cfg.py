import FWCore.ParameterSet.Config as cms

process = cms.Process("Ana")
process.load('FWCore.MessageService.MessageLogger_cfi')
##-------------------- Communicate with the DB -----------------------
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.GlobalTag.globaltag = 'FT_53_V21_AN6::All'
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.Geometry.GeometryIdeal_cff')
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
    input = cms.untracked.int32(1000)
)
#############   Format MessageLogger #################
process.MessageLogger.cerr.FwkReport.reportEvery = 10000
#############   Define the source file ###############
process.source = cms.Source("PoolSource",
#    fileNames = cms.untracked.vstring('/store/data/Run2012C/JetHT/AOD/PromptReco-v2/000/198/941/221BEAC8-7ACF-E111-8A3D-E0CB4E4408E7.root')
   fileNames = cms.untracked.vstring(
'/store/data/Run2015B/JetHT/MINIAOD/PromptReco-v1/000/251/562/00000/26A914E6-9C2A-E511-AC57-02163E011CD6.root',
'/store/data/Run2015B/JetHT/MINIAOD/PromptReco-v1/000/251/562/00000/48102A76-7D2A-E511-A753-02163E011E24.root',
'/store/data/Run2015B/JetHT/MINIAOD/PromptReco-v1/000/251/562/00000/508117F0-9C2A-E511-A71B-02163E014241.root',
'/store/data/Run2015B/JetHT/MINIAOD/PromptReco-v1/000/251/562/00000/6C284BEF-9C2A-E511-A00C-02163E013536.root',
'/store/data/Run2015B/JetHT/MINIAOD/PromptReco-v1/000/251/562/00000/704086DE-9C2A-E511-83FF-02163E014576.root',
'/store/data/Run2015B/JetHT/MINIAOD/PromptReco-v1/000/251/562/00000/720AC5E7-9C2A-E511-9FB2-02163E0129A3.root',
'/store/data/Run2015B/JetHT/MINIAOD/PromptReco-v1/000/251/562/00000/8400ADFB-842A-E511-AF09-02163E01420D.root',
'/store/data/Run2015B/JetHT/MINIAOD/PromptReco-v1/000/251/562/00000/8A33C3E4-9C2A-E511-95EC-02163E0123C0.root',
'/store/data/Run2015B/JetHT/MINIAOD/PromptReco-v1/000/251/562/00000/924A8CCD-802A-E511-AFEE-02163E0125E8.root',
'/store/data/Run2015B/JetHT/MINIAOD/PromptReco-v1/000/251/562/00000/B6E35572-822A-E511-B0E4-02163E0136E6.root',
'/store/data/Run2015B/JetHT/MINIAOD/PromptReco-v1/000/251/562/00000/C67C9591-8E2A-E511-9D3D-02163E014275.root',
'/store/data/Run2015B/JetHT/MINIAOD/PromptReco-v1/000/251/562/00000/CE70BD25-862A-E511-924E-02163E011824.root',
'/store/data/Run2015B/JetHT/MINIAOD/PromptReco-v1/000/251/562/00000/CEF44D82-882A-E511-AED0-02163E013597.root',
       )
)
############# processed tree producer ##################
process.TFileService = cms.Service("TFileService",fileName = cms.string('TriggerAna_data.root'))






process.trigAna = cms.EDAnalyzer('TriggerAnaPlugin',
    ## trigger ###################################
    bits = cms.InputTag("TriggerResults","","HLT"),
    prescales = cms.InputTag("patTrigger"),
    objects = cms.InputTag("selectedPatTrigger"),
    triggerNames     = cms.vstring('HLT_PFJet40_v2', 'HLT_PFJet40_v3', 'HLT_PFJet40_v4','HLT_PFJet40_v5','HLT_PFJet40_v6','HLT_PFJet40_v7','HLT_PFJet40_v8','HLT_PFJet40_v9',
                                   'HLT_PFJet80_v2', 'HLT_PFJet80_v3', 'HLT_PFJet80_v4','HLT_PFJet80_v5','HLT_PFJet80_v6','HLT_PFJet80_v7','HLT_PFJet80_v8','HLT_PFJet80_v9',
                                   'HLT_PFJet140_v2','HLT_PFJet140_v3','HLT_PFJet140_v4','HLT_PFJet140_v5','HLT_PFJet140_v6','HLT_PFJet140_v7','HLT_PFJet140_v8','HLT_PFJet140_v9',
                                   'HLT_PFJet200_v2','HLT_PFJet200_v3','HLT_PFJet200_v4','HLT_PFJet200_v5','HLT_PFJet200_v6','HLT_PFJet200_v7','HLT_PFJet200_v8','HLT_PFJet200_v9',
                                   'HLT_PFJet260_v2','HLT_PFJet260_v3','HLT_PFJet260_v4','HLT_PFJet260_v5','HLT_PFJet260_v6','HLT_PFJet260_v7','HLT_PFJet260_v8','HLT_PFJet260_v9',
                                   'HLT_PFJet320_v2','HLT_PFJet320_v3','HLT_PFJet320_v4','HLT_PFJet320_v5','HLT_PFJet320_v6','HLT_PFJet320_v7','HLT_PFJet320_v8','HLT_PFJet320_v9',
                                   'HLT_PFJet400_v2','HLT_PFJet400_v3','HLT_PFJet400_v4','HLT_PFJet400_v5','HLT_PFJet400_v6','HLT_PFJet400_v7','HLT_PFJet400_v8','HLT_PFJet400_v9',
                                   'HLT_PFJet450_v2','HLT_PFJet450_v3','HLT_PFJet450_v4','HLT_PFJet450_v5','HLT_PFJet450_v6','HLT_PFJet450_v7','HLT_PFJet450_v8','HLT_PFJet450_v9',
                                   'HLT_PFJet500_v2','HLT_PFJet500_v3','HLT_PFJet500_v4','HLT_PFJet500_v5','HLT_PFJet500_v6','HLT_PFJet500_v7','HLT_PFJet500_v8','HLT_PFJet500_v9',
    ),

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

