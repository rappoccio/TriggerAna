#include <iostream>
#include <sstream>
#include <istream>
#include <fstream>
#include <iomanip>
#include <string>
#include <cmath>
#include <functional>
#include "TTree.h"
#include <vector>
#include <cassert>
#include <TLorentzVector.h>
#include "Analysis/TriggerAna/plugins/TriggerAnaPlugin.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "FWCore/Common/interface/TriggerResultsByName.h"
#include "DataFormats/Common/interface/Handle.h"

using namespace std;
using namespace edm;

TriggerAnaPlugin::TriggerAnaPlugin(edm::ParameterSet const& cfg)
{
  mPrintTriggerMenu  = cfg.getUntrackedParameter<bool>             ("printTriggerMenu",false);
  processName_       = cfg.getParameter<std::string>               ("processName");
  triggerNames_      = cfg.getParameter<std::vector<std::string> > ("triggerName");
  triggerResultsTag_ = cfg.getParameter<edm::InputTag>             ("triggerResults");
  triggerEventTag_   = cfg.getParameter<edm::InputTag>             ("triggerEvent");

  event_ = 0;
  run_ = 0;
  lumiBlock_ = 0;

  Fired_.clear();
  TriggerDecision_.clear();
  triggerList_.clear(); 
  L1Prescales_.clear();
  HLTPrescales_.clear();

}
//////////////////////////////////////////////////////////////////////////////////////////
void TriggerAnaPlugin::beginJob()
{

  Fired_.clear();
  TriggerDecision_.clear();
  triggerList_.clear(); 
  L1Prescales_.clear();
  HLTPrescales_.clear();

  mTree = fs->make<TTree>("TrigTree","TrigTree");
  
  mTree->Branch("run",   &run_);
  mTree->Branch("event", &event_);
  mTree->Branch("lumiBlock",  &lumiBlock_);
  mTree->Branch("Fired", &Fired_);
  mTree->Branch("TriggerDecision", &TriggerDecision_);
  mTree->Branch("triggerList", &triggerList_);
  mTree->Branch("L1Prescales", &L1Prescales_);
  mTree->Branch("HLTPrescales", &HLTPrescales_);


  mTriggerNamesHisto = fs->make<TH1F>("TriggerNames","TriggerNames",1,0,1);
  mTriggerNamesHisto->SetBit(TH1::kCanRebin);
  for(unsigned i=0;i<triggerNames_.size();i++)
    mTriggerNamesHisto->Fill(triggerNames_[i].c_str(),1);
  mTriggerPassHisto = fs->make<TH1F>("TriggerPass","TriggerPass",1,0,1);
  mTriggerPassHisto->SetBit(TH1::kCanRebin);
}
//////////////////////////////////////////////////////////////////////////////////////////
void TriggerAnaPlugin::endJob()
{
}
//////////////////////////////////////////////////////////////////////////////////////////
void TriggerAnaPlugin::beginRun(edm::Run const & iRun, edm::EventSetup const& iSetup)
{
  bool changed(true);
  if (hltConfig_.init(iRun,iSetup,processName_,changed)) {
    if (changed) {
      // check if trigger names in (new) config
      cout<<"New trigger menu found !!!"<<endl;
      triggerIndex_.clear();
      const unsigned int n(hltConfig_.size());
      for(unsigned itrig=0;itrig<triggerNames_.size();itrig++) {
        triggerIndex_.push_back(hltConfig_.triggerIndex(triggerNames_[itrig]));
        cout<<triggerNames_[itrig]<<" "<<triggerIndex_[itrig]<<" ";
	if (triggerIndex_[itrig] >= n)
          cout<<"does not exist in the current menu"<<endl;
	else
          cout<<"exists"<<endl;
      }
      cout << "Available TriggerNames are: " << endl;
      if (mPrintTriggerMenu)
        hltConfig_.dump("Triggers");
    }
  }
  else {
    cout << "TriggerAnaPlugin::analyze:"
         << " config extraction failure with process name "
         << processName_ << endl;
  }
}
//////////////////////////////////////////////////////////////////////////////////////////
void TriggerAnaPlugin::analyze(edm::Event const& event, edm::EventSetup const& iSetup)
{

  Fired_.clear();
  TriggerDecision_.clear();
  triggerList_.clear();
  L1Prescales_.clear();
  HLTPrescales_.clear();

  //-------------- Basic Event Info ------------------------------
  run_ = event.id().run();
  event_ = event.id().event();
  lumiBlock_ = event.luminosityBlock();

  //-------------- Trigger Info -----------------------------------
  event.getByLabel(triggerResultsTag_,triggerResultsHandle_);
  if (!triggerResultsHandle_.isValid()) {
    cout << "TriggerAnaPlugin::analyze: Error in getting TriggerResults product from Event!" << endl;
    return;
  }
  event.getByLabel(triggerEventTag_,triggerEventHandle_);
  if (!triggerEventHandle_.isValid()) {
    cout << "TriggerAnaPlugin::analyze: Error in getting TriggerEvent product from Event!" << endl;
    return;
  }

  // sanity check
  assert(triggerResultsHandle_->size() == hltConfig_.size());
  //------ loop over all trigger names ---------
  for(unsigned itrig=0;itrig<triggerNames_.size();itrig++) {
    bool accept(false);
    int preL1(-1);
    int preHLT(-1);
    int tmpFired(-1);
    if (triggerIndex_[itrig] < hltConfig_.size()) {
      accept = triggerResultsHandle_->accept(triggerIndex_[itrig]);
      //      const std::pair<int,int> prescales(hltConfig_.prescaleValues(event,iSetup,triggerNames_[itrig]));
      ///In detail
      //get prescale info from hltConfig_
      std::pair<std::vector<std::pair<std::string,int> >,int> detailedPrescaleInfo = hltConfig_.prescaleValuesInDetail(event, iSetup, triggerNames_[itrig]);	 
      preHLT = detailedPrescaleInfo.second ;
      // save l1 prescale values in standalone vector
      std::vector <int> l1prescalevals;
      for( size_t varind = 0; varind < detailedPrescaleInfo.first.size(); varind++ ){
	l1prescalevals.push_back(detailedPrescaleInfo.first.at(varind).second);
      }
      // find and save minimum l1 prescale of any ORed L1 that seeds the HLT
      std::vector<int>::iterator result = std::min_element(std::begin(l1prescalevals), std::end(l1prescalevals));
      size_t minind = std::distance(std::begin(l1prescalevals), result);
      // sometimes there are no L1s associated with a HLT. In that case, this branch stores -1 for the l1prescale
      //l1prescales->push_back( minind < l1prescalevals.size() ? l1prescalevals.at(minind) : -1 );
      preL1 = minind < l1prescalevals.size() ? l1prescalevals.at(minind) : -1 ;
      ///end in detail
      //      preL1    = prescales.first;
      ///      preHLT   = prescales.second;
      if (!accept)
        tmpFired = 0;
      else {
	mTriggerPassHisto->Fill(triggerNames_[itrig].c_str(),1);
        tmpFired = 1;
      }

    }// if the trigger exists in the menu
    //cout<<triggerNames_[itrig]<<" "<<triggerIndex_[itrig]<<" "<<accept<<" "<<tmpFired<<endl;
    Fired_.push_back(tmpFired);
    L1Prescales_.push_back(preL1);
    HLTPrescales_.push_back(preHLT);
  }// loop over trigger names


  mTree->Fill();
}
//////////////////////////////////////////////////////////////////////////////////////////
TriggerAnaPlugin::~TriggerAnaPlugin()
{
}
DEFINE_FWK_MODULE(TriggerAnaPlugin);
