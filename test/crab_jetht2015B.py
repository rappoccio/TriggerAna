from WMCore.Configuration import Configuration
config = Configuration()

config.section_("General")
config.General.requestName = 'jetht2015B'
config.General.workArea = 'SMPJ_TriggerAna'
config.General.transferLogs = True

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'triggerAna_cfg.py'

config.section_("Data")
config.Data.inputDataset = '/JetHT/Run2015B-PromptReco-v1/AOD' 
config.Data.splitting = 'LumiBased'
config.Data.lumiMask = 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions15/13TeV/Cert_246908-251252_13TeV_PromptReco_Collisions15_JSON.txt'
config.Data.unitsPerJob = 100
config.Data.ignoreLocality = True
config.Data.publication = False
# This string is used to construct the output dataset name
#config.Data.publishDBS = 'phys03'
#config.Data.publishDataName = 'B2GAnaFW_v74x_V4'

config.section_("Site")
config.Site.storageSite = 'T3_US_FNALLPC'

