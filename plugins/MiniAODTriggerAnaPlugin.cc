// system include files
#include <memory>
#include <cmath>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Math/interface/deltaR.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/PatCandidates/interface/TriggerObjectStandAlone.h"
#include "DataFormats/PatCandidates/interface/PackedTriggerPrescales.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "TTree.h"

class MiniAODTriggerAnaPlugin : public edm::EDAnalyzer {
   public:
      explicit MiniAODTriggerAnaPlugin(const edm::ParameterSet&);
      ~MiniAODTriggerAnaPlugin() {}
      void beginJob();

   private:
      virtual void analyze(const edm::Event&, const edm::EventSetup&) override;

      edm::EDGetTokenT<edm::TriggerResults> triggerBits_;
      edm::EDGetTokenT<pat::TriggerObjectStandAloneCollection> triggerObjects_;
      edm::EDGetTokenT<pat::PackedTriggerPrescales> triggerPrescales_;

      std::vector<std::string> triggerNames_;

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

MiniAODTriggerAnaPlugin::MiniAODTriggerAnaPlugin(const edm::ParameterSet& iConfig):
    triggerBits_(consumes<edm::TriggerResults>(iConfig.getParameter<edm::InputTag>("bits"))),
    triggerObjects_(consumes<pat::TriggerObjectStandAloneCollection>(iConfig.getParameter<edm::InputTag>("objects"))),
    triggerPrescales_(consumes<pat::PackedTriggerPrescales>(iConfig.getParameter<edm::InputTag>("prescales"))),
    triggerNames_(iConfig.getParameter< std::vector<std::string> >("triggerNames"))
{


  event_ = 0;
  run_ = 0;
  lumiBlock_ = 0;

  Fired_.clear();
  TriggerDecision_.clear();
  triggerList_.clear(); 
  L1Prescales_.clear();
  HLTPrescales_.clear();
}


void MiniAODTriggerAnaPlugin::beginJob()
{

  mTree = fs->make<TTree>("TrigTree","TrigTree");
  
  mTree->Branch("run",   &run_);
  mTree->Branch("event", &event_);
  mTree->Branch("lumiBlock",  &lumiBlock_);
  mTree->Branch("Fired", &Fired_);
  mTree->Branch("TriggerDecision", &TriggerDecision_);
  mTree->Branch("triggerList", &triggerList_);
  mTree->Branch("L1Prescales", &L1Prescales_);
  mTree->Branch("HLTPrescales", &HLTPrescales_);

}


void MiniAODTriggerAnaPlugin::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{


  event_ = 0;
  run_ = 0;
  lumiBlock_ = 0;

  Fired_.clear();
  TriggerDecision_.clear();
  triggerList_.clear(); 
  L1Prescales_.clear();
  HLTPrescales_.clear();

  edm::Handle<edm::TriggerResults> triggerBits;
  edm::Handle<pat::TriggerObjectStandAloneCollection> triggerObjects;
  edm::Handle<pat::PackedTriggerPrescales> triggerPrescales;

  iEvent.getByToken(triggerBits_, triggerBits);
  iEvent.getByToken(triggerObjects_, triggerObjects);
  iEvent.getByToken(triggerPrescales_, triggerPrescales);

  const edm::TriggerNames &names = iEvent.triggerNames(*triggerBits);
  std::cout << "\n === TRIGGER PATHS === " << std::endl;
  for (unsigned int i = 0, n = triggerBits->size(); i < n; ++i) {
    auto const & name = names.triggerName(i);
    auto const & prescale = triggerPrescales->getPrescaleForIndex(i);
    auto const & fired = triggerBits->accept(i);

    if ( std::find_if(triggerNames_.begin(), triggerNames_.end(), [name](std::string const & n) { return n.find(name) != std::string::npos; } ) != triggerNames_.end() ) {
      std::cout << "Trigger " << names.triggerName(i) << 
	", prescale " << prescale <<
	": " << (fired ? "PASS" : "fail (or not run)")  << std::endl;
      Fired_.push_back( fired );
      triggerList_.push_back( name );
      HLTPrescales_.push_back( prescale );
    }
  }


  mTree->Fill();

}

//define this as a plug-in
DEFINE_FWK_MODULE(MiniAODTriggerAnaPlugin);

