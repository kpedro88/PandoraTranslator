import FWCore.ParameterSet.Config as cms

from RecoLocalCalo.CaloTowersCreator.calotowermaker_cfi import *

process = cms.Process("Demo")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.load("RecoLocalCalo.CaloTowersCreator.calotowermaker_cfi")

# No data of type "HGCalGeometry" with label "HGCalEESensitive" in record "IdealGeometryRecord"
process.load('Configuration.Geometry.GeometryExtended2023HGCalMuonReco_cff')

#The below three lines were added to solve an error Exception Message:
#No "CaloGeometryRecord" record found in the EventSetup.
### process.load("Geometry.CMSCommonData.cmsIdealGeometryXML_cfi");
### process.load("Geometry.CaloEventSetup.CaloGeometry_cfi");
### process.load("Geometry.CaloEventSetup.CaloTopology_cfi");

#Add the next two lines to solve an error Exception Message:
#No "IdealMagneticFieldRecord" record found in the EventSetup.
### process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")

#Add the next three lines to solve an error Exception Message:
#No "TransientTrackRecord" record found in the EventSetup.
process.load("TrackingTools/TransientTrack/TransientTrackBuilder_cfi")
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:upgradePLS3', '')
# process.GlobalTag.globaltag = 'START70_V1::All'

process.TrackAssociatorRecord = cms.ESSource("EmptyESSource",
        recordName = cms.string('TrackAssociatorRecord'),
        iovIsRunNotTime = cms.bool(True),
        firstValid = cms.vuint32(1)
)
process.load('SimTracker.TrackAssociation.quickTrackAssociatorByHits_cfi')

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

# this is for the event display 
#process.EveService = cms.Service("EveService")

from particleFileLists import Pho100

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
#        'file:/afs/cern.ch/work/v/vandreev/public/RecHits/SLHC14/step3_elecPt35.root'
#        'file:/afs/cern.ch/work/a/apsallid/public/step3_SinglePiPt100_EtaEE.root'
#	 'file:/afs/cern.ch/work/a/apsallid/public/step3_SingleElectronPt35_EtaEE.root'
#        'file:/afs/cern.ch/work/a/apsallid/public/step3_SingleMuPt10_EtaEE.root'
#	 'file:/afs/cern.ch/work/a/apsallid/public/step3_SinglePiPt10_EtaEE.root'

#	 'file:/afs/cern.ch/work/a/apsallid/public/step3_SinglePiPt10.root'
#        'file:/afs/cern.ch/work/a/apsallid/public/step3_SinglePiPt20.root'
#        'file:/afs/cern.ch/work/a/apsallid/public/step3_SingleElectronPt35.root'
#        'file:/afs/cern.ch/work/a/apsallid/public/step3_SingleGammaPt35.root'
#        'file:/afs/cern.ch/user/l/lgray/work/private/CMSSW_6_2_0_SLHC23_patch2/src/matrix_tests/step3.root'
#         'root://eoscms//eos/cms/store/group/phys_b2g/apsallid/hg/SinglePiPt10/Step3Files/step3_2.root' 
#        'file:/afs/cern.ch/work/a/apsallid/public/step3_SingleElectronPt50.root'
#        'file:/afs/cern.ch/work/a/apsallid/public/step3_SinglePi0E20.root'
#	 'file:/afs/cern.ch/user/l/lgray/work/public/CMSSW_6_2_X_SLHC_2014-07-17-0200/src/matrix_tests/140_pu/step3.root'
#        "/store/cmst3/group/hgcal/CMSSW/Single22_CMSSW_6_2_0_SLHC23_patch1/RECO-PU0/Events_22_20_80.root"
        Pho100 # all photon files, 100 GeV
    )
)

process.source.skipEvents = cms.untracked.uint32(0)

process.load('SimGeneral.MixingModule.mixNoPU_cfi')                                                                                                                               
process.load("Configuration.StandardSequences.Reconstruction_cff")
process.load("RecoParticleFlow/PFClusterProducer/particleFlowRecHitHGCEE_cfi")
process.load("RecoParticleFlow/PFClusterProducer/particleFlowRecHitECAL_cfi")
process.load("RecoParticleFlow/PFClusterProducer/particleFlowRecHitHBHE_cfi")

process.trackingParticleRecoTrackAsssociation = cms.EDProducer(
    "TrackAssociatorEDProducer",
    label_tr = cms.InputTag("generalTracks"),
    associator = cms.string('quickTrackAssociatorByHits'),
    label_tp = cms.InputTag("mix","MergedTrackTruth"),
    ignoremissingtrackcollection = cms.untracked.bool(False)
    )

process.pandorapfanew = cms.EDProducer('PandoraCMSPFCandProducer',
    ecalRecHitsEB = cms.InputTag("particleFlowRecHitECAL",""),
    hcalRecHitsHBHE = cms.InputTag("particleFlowRecHitHBHE",""),
    HGCrechitCollection  = cms.InputTag("particleFlowRecHitHGCEE",""), 
    generaltracks = cms.VInputTag(cms.InputTag("generalTracks")),
    tPRecoTrackAsssociation= cms.InputTag("trackingParticleRecoTrackAsssociation"),
    genParticles= cms.InputTag("genParticles"),
#    inputconfigfile = cms.string('PandoraSettingsDefault_WithoutMonitoring.xml'),
#    inputconfigfile = cms.string('PandoraSettingsDefault.xml'),
#    inputconfigfile = cms.string('PandoraSettingsBasic.xml'),
    inputconfigfile = cms.FileInPath('HGCal/PandoraTranslator/data/PandoraSettingsBasic_cms.xml'),
#    inputconfigfile = cms.string('PandoraSettingsMuon.xml')

    energyCorrMethod = cms.string('ABSCORR'),
#   absorber thickness correction
#   energyCorrMethod = cms.string('WEIGHTING'),
    energyWeightFile = cms.FileInPath('HGCal/PandoraTranslator/data/energyWeight.txt'),

    calibrParFile = cms.FileInPath('HGCal/PandoraTranslator/data/pandoraCalibrPars.txt'),
    layerDepthFile = cms.FileInPath('HGCal/PandoraTranslator/data/HGCmaterial_v5.root'),
    overburdenDepthFile = cms.FileInPath('RecoParticleFlow/PFClusterProducer/data/HGCMaterialOverburden.root'),
    useOverburdenCorrection = cms.bool(False), #disabled until the overburden values make sense
    outputFile = cms.string('pandoraoutput.root')
)

# To use the hgcTrackerInteractionsFilter, you need the following additional code
#
# cd ${CMSSW_BASE}/src
# git clone https://github.com/sethzenz/HGCanalysis.git UserCode/HGCanalysis
# git checkout origin/hacked-interactions-filter
# cd Usercode ; scram b -j 9

process.load("UserCode/HGCanalysis/hgcTrackerInteractionsFilter_cfi")

process.reconstruction_step = cms.Path(process.trackerIntFilter*
                                       process.particleFlowRecHitHGCEE*
                                       process.particleFlowRecHitHBHE*
                                       process.particleFlowRecHitECAL*
                                       process.trackingParticleRecoTrackAsssociation*
                                       process.pandorapfanew)
process.schedule = cms.Schedule(process.reconstruction_step)
from SLHCUpgradeSimulations.Configuration.combinedCustoms import cust_2023HGCalMuon
process = cust_2023HGCalMuon(process)

