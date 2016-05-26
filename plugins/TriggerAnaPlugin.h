#ifndef AnalysisTriggerAnaPlugin_h
#define AnalysisTriggerAnaPlugin_h

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "HLTrigger/HLTcore/interface/HLTConfigProvider.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/HLTReco/interface/TriggerEvent.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"


class TriggerAnaPlugin : public edm::EDAnalyzer
{
 public:
  typedef reco::Particle::LorentzVector LorentzVector;
  explicit TriggerAnaPlugin(edm::ParameterSet const& cfg);
  virtual void beginJob();
  virtual void beginRun(edm::Run const &, edm::EventSetup const& iSetup);
  virtual void analyze(edm::Event const& evt, edm::EventSetup const& iSetup);
  virtual void endJob();
  virtual ~TriggerAnaPlugin();
 private:
  void buildTree();
  //---- configurable parameters --------
  bool   mPrintTriggerMenu;

  //---- TRIGGER -------------------------
  std::string   processName_;
  std::vector<std::string> triggerNames_;
  std::vector<unsigned int> triggerIndex_;
  edm::InputTag triggerResultsTag_;
  edm::InputTag triggerEventTag_;
  edm::Handle<edm::TriggerResults>   triggerResultsHandle_;
  edm::Handle<trigger::TriggerEvent> triggerEventHandle_;
  HLTConfigProvider hltConfig_;

  edm::Service<TFileService> fs;
  TTree *mTree;
  TH1F *mTriggerPassHisto,*mTriggerNamesHisto;

  unsigned int event_;
  unsigned int run_;
  unsigned int lumiBlock_;

  std::vector<int>         Fired_;
  std::vector<int>         TriggerDecision_;
  std::vector<std::string> triggerList_; 
  std::vector<int>         L1Prescales_;
  std::vector<int>         HLTPrescales_;


};

#endif
