import os
import csv
import copy
import inspect
import numpy as np

configurations = os.path.realpath(inspect.getfile(inspect.currentframe())) # this file
configurations = os.path.dirname(configurations) # Full2016v7
configurations = os.path.dirname(configurations) # HM
configurations = os.path.dirname(configurations) # Configurations

#aliases = {}

# imported from samples.py:
# samples, signals

mc = [skey for skey in samples if skey not in ('FAKE', 'DATA')]
wjets = [skey for skey in samples if skey.startswith('Wjets')]

eleWP    = 'mva_90p_Iso2016'
muWP     = 'cut_Tight80x'

#aliases['DNN_isVBF_OTF'] = {
#    'class': 'DNNprodSemi',
#    'linesToAdd':[
#        'gSystem->Load("libLatinoAnalysisMultiDraw.so")',
#        'gSystem->Load("libDNNEvaluator.so")',
#        '.L %s/src/PlotsConfigurations/Configurations/HighMass/DNN_prod_semi.cc+' % os.getenv('CMSSW_BASE'),
#    ],
#}

#aliases['btagJetPt_resolv'] = {
 #   'linesToAdd': [
 #       '.L %s/src/PlotsConfigurations/Configurations/HWWSemiLepHighMass/btagJetPt.cc+' % os.getenv('CMSSW_BASE')
 #   ],
 #   'class': 'BtagJetPt',
 #   'args': ('resolved', '2016')
#}
#aliases['btagJetPt_boost'] = {
 #   'linesToAdd': [
  #      '.L %s/src/PlotsConfigurations/Configurations/HWWSemiLepHighMass/btagJetPt.cc+' % os.getenv('CMSSW_BASE')
   # ],
   # 'class': 'BtagJetPt',
   # 'args': ('boosted', '2016')
#}

aliases['mjjGen_OTF'] = {
    'linesToAdd': ['.L %s/src/PlotsConfigurations/Configurations/HighMass/HMvars_mjjgen.cc+' % os.getenv('CMSSW_BASE')],
    'class': 'HMvarsmjjgen',
    'samples': [skey for skey in samples if "QQHSBI" in skey or skey in ['WW', 'qqWWqq', 'WW2J', 'DYveto']]
}

aliases['bWP'] = {
    'expr': '0.2217'
}
aliases['tau21WP'] = {
    'expr': '0.4'
}
aliases['LepWPCut'] = {
    'expr': '(Lepton_isTightElectron_'+eleWP+'[0] > 0.5 \
            || Lepton_isTightMuon_'+muWP+'[0] > 0.5)'
}
aliases['Lep1WPCut'] = {
    'expr': '(Alt$(Lepton_isTightElectron_'+eleWP+'[1], 0) > 0.5 \
            || Alt$(Lepton_isTightMuon_'+muWP+'[1], 0) > 0.5)'
}
aliases['nTightLep'] = {
    'expr': '(Sum$(Lepton_isTightElectron_'+eleWP+') + Sum$(Lepton_isTightMuon_'+muWP+'))',
}


aliases['resolvHiggsMT'] = {
    # 'expr': 'HM_Hlnjj_mt'
    'expr': 'TMath::Sqrt( 2*Lepton_pt[0]*PuppiMET_pt \
    *( 1-TMath::Cos(Lepton_phi[0]-PuppiMET_phi) ) )'
}

aliases['HM_Hlnjj_MT'] = {
    # 'expr': 'HM_Hlnjj_mt'
    'expr': 'TMath::Sqrt( 2*HM_Wlep_pt_Puppi*HM_Whad_pt \
    *( 1-TMath::Cos(HM_Wlep_phi_Puppi-HM_Whad_phi) ) )'
}

#aliases['WptOvFat_nocut'] = {
#    # 'expr': 'HM_Hlnjj_mt'
#    'expr': ' TMath::Sqrt( 2*HM_Wlep_pt_Puppi*HM_Whad_pt)'
#}
#
#
#aliases['WptOvHak4M_nocut'] = {
#    'expr': 'min(HM_Wlep_pt_Puppi,HM_Whad_pt)/Hlnjj_mass_HM' 
#}
#

aliases['idxCleanFatJetW'] = {
    'expr': '(HM_idxWfat_noTau21Cut*(HM_idxWfat_noTau21Cut>=0) + 999*(HM_idxWfat_noTau21Cut<0))'
}

aliases['tau21Cut'] = {
    'expr': '(Alt$(CleanFatJet_tau21[idxCleanFatJetW], 1) < tau21WP)'
}

aliases['boosted'] = {
    'expr': 'PuppiMET_pt > 40 \
            && Alt$(HM_CleanFatJetPassMBoosted_pt[0], 0) > 200 \
            && Alt$(HM_CleanFatJetPassMBoosted_WptOvHfatM[0], 0) > 0.4 \
            && Alt$(HM_CleanFatJetPassMBoosted_tau21[0], 999) < tau21WP[0] \
            && Alt$(HM_CleanFatJetPassMBoosted_mass[0], 0) > 40 \
            && abs(Alt$(HM_CleanFatJetPassMBoosted_eta[0], 999)) < 2.4'
}
aliases['boostedNoTau21'] = {
    'expr': 'PuppiMET_pt > 40 \
            && idxCleanFatJetW != 999 \
            && Alt$(CleanFatJet_pt[idxCleanFatJetW], 0) > 200 \
            && Alt$(CleanFatJet_pt[idxCleanFatJetW], 0) / HM_HlnFatMass_noTau21Cut > 0.4 \
            && HM_HlnFatMass_noTau21Cut > 0 && HM_Wlep_pt_Puppi / HM_HlnFatMass_noTau21Cut > 0.4 \
            && Alt$(CleanFatJet_mass[idxCleanFatJetW], 0) > 40 \
            && Alt$(CleanFatJet_eta[idxCleanFatJetW], 999) < 2.4'
}

aliases['resolved'] = {
    'expr': '!boosted[0] \
            && PuppiMET_pt > 30 \
            && HM_WptOvHak4M > 0.35 \
            && resolvHiggsMT > 60 \
            && HM_Whad_pt > 30'
}

aliases['boostedSignalWMass'] = {
    'expr': '(65 < Alt$(CleanFatJet_mass[0], 0) \
            && Alt$(CleanFatJet_mass[0], 999) < 105)'
}
aliases['boostedSignalWMassNoTau21'] = {
    'expr': '(65 < Alt$(CleanFatJet_mass[idxCleanFatJetW], 0) \
            && Alt$(CleanFatJet_mass[idxCleanFatJetW], 999) < 105)'
}

aliases['resolvedSignalWMass'] = {
    'expr': '(65 < HM_Whad_mass && HM_Whad_mass < 105)'
}

aliases['boostedSidebandWMass'] = {
    'expr': '(40 < Alt$(CleanFatJet_mass[0], 0) \
            && Alt$(CleanFatJet_mass[0], 999) < 250)'
}
aliases['boostedSidebandWMassNoTau21'] = {
    'expr': '(40 < Alt$(CleanFatJet_mass[idxCleanFatJetW], 0) \
            && Alt$(CleanFatJet_mass[idxCleanFatJetW], 999) < 250)'
}

aliases['lowBoostedSidebandWMass'] = {
    'expr': '(40 < Alt$(HM_CleanFatJetPassMBoosted_mass[0], 0) \
            && Alt$(HM_CleanFatJetPassMBoosted_mass[0], 999) < 65)'
}
aliases['highBoostedSidebandWMass'] = {
    'expr': '(105 < Alt$(HM_CleanFatJetPassMBoosted_mass[0], 0) \
            && Alt$(HM_CleanFatJetPassMBoosted_mass[0], 999) < 250)'
}


aliases['resolvedSidebandWMass'] = {
    'expr': '(40 < HM_Whad_mass && HM_Whad_mass < 250)'
}

aliases['lowResolvedSidebandWMass'] = {
    'expr': '(40 < HM_Whad_mass && HM_Whad_mass < 65)'
}
aliases['highResolvedSidebandWMass'] = {
    'expr': '(105 < HM_Whad_mass && HM_Whad_mass < 250)'
}






aliases['resolvedQCDcr'] = {
    'expr': 'resolvedSignalWMass \
            && HM_Wlep_mt < 50 && 0 < resolvHiggsMT \
            && resolvHiggsMT < 60 && HM_WptOvHak4M < 0.35'
}
aliases['resolvedQCDSR'] = {
    'expr': '!boosted[0] \
            && resolvedSignalWMass \
            && PuppiMET_pt > 30 \
            && HM_WptOvHak4M > 0.35 \
            && resolvHiggsMT > 60 \
            && HM_Whad_pt > 30'
}
# boostedQCDcr not possible RN since boosted W candidate always fulfills WptOvHfatM > 0.4


aliases['tau21DDT'] = {
    'expr': '( Alt$(CleanFatJet_tau21[idxCleanFatJetW], -999) + 0.080 * TMath::Log( Alt$(CleanFatJet_mass[idxCleanFatJetW]*CleanFatJet_mass[idxCleanFatJetW], 0) / Alt$(CleanFatJet_pt[idxCleanFatJetW], 1) ) )'
}
# smaller angle is: a-b - (a-b > 3.1416)*2*3.1416 + (a-b < -3.1416)*2*3.1416
aliases['dPhi_WW_boosted'] = {
    'expr': '( HM_Wlep_phi_Puppi - Alt$(HM_CleanFatJetPassMBoosted_phi[0], 0)\
- (HM_Wlep_phi_Puppi - Alt$(HM_CleanFatJetPassMBoosted_phi[0], 0) > 3.1416)*2*3.1416\
+ (HM_Wlep_phi_Puppi - Alt$(HM_CleanFatJetPassMBoosted_phi[0], 0) < -3.1416)*2*3.1416 )',
}
aliases['dPhi_WW_resolved'] = {
    'expr': '( HM_Wlep_phi_Puppi - HM_Whad_phi\
    - (HM_Wlep_phi_Puppi - HM_Whad_phi > 3.1416)*2*3.1416 \
    + (HM_Wlep_phi_Puppi - HM_Whad_phi < -3.1416)*2*3.1416 )',
}
aliases['dPhi_LNu'] = {
    'expr': '( Lepton_phi[0] - PuppiMET_phi\
    - (Lepton_phi[0] - PuppiMET_phi > 3.1416)*2*3.1416 \
    + (Lepton_phi[0] - PuppiMET_phi < -3.1416)*2*3.1416 )',
}

aliases['deltaR'] = {
    'expr' : 'TMath::Sqrt((HM_Whad_phi - Alt$(CleanFatJet_phi[0],0))*(HM_Whad_phi - Alt$(CleanFatJet_phi[0],0)) + (HM_Whad_eta - Alt$(CleanFatJet_eta[0],0))*(HM_Whad_eta - Alt$(CleanFatJet_eta[0],0))) '
}

aliases['mass_HIGGS_FAT'] = {
    'linesToAdd':['.L %s/src/PlotsConfigurations/Configurations/HWWSemiLepHighMass/getResBoo.cc+'  % os.getenv('CMSSW_BASE')],
    'class': 'getResBoo',
    'args': 0
}

aliases['HvOverFat'] = {
    'linesToAdd':['.L %s/src/PlotsConfigurations/Configurations/HWWSemiLepHighMass/getResBoo.cc+'  % os.getenv('CMSSW_BASE')],
    'class': 'getResBoo',
    'args': 1
}

aliases['mass_HIGGS_JJ'] = {
    'linesToAdd':['.L %s/src/PlotsConfigurations/Configurations/HWWSemiLepHighMass/getResBoo.cc+'  % os.getenv('CMSSW_BASE')],
    'class': 'getResBoo',
    'args': 2
}

aliases['HvOverJJ'] = {
    'linesToAdd':['.L %s/src/PlotsConfigurations/Configurations/HWWSemiLepHighMass/getResBoo.cc+'  % os.getenv('CMSSW_BASE')],
    'class': 'getResBoo',
    'args': 3
}

aliases['HvOverLEP'] = {
    'linesToAdd':['.L %s/src/PlotsConfigurations/Configurations/HWWSemiLepHighMass/getResBoo.cc+'  % os.getenv('CMSSW_BASE')],
    'class': 'getResBoo',
    'args': 4
}

aliases['cohe_jet'] ={
    'expr': 'deltaR < 1 \
            && nCleanFatJet >= 1 \
            && nCleanJet >= 2 \
            && CleanJet_pt[0] > 30 \
            && CleanJet_pt[1] > 30 \
            && PuppiMET_pt[0] > 40 \
            && Alt$(CleanFatJet_pt[idxCleanFatJetW], 0) > 200 \
            && Alt$(CleanFatJet_eta[idxCleanFatJetW], 999) < 2.4'
}


aliases['fat_jet'] ={
    'expr': 'nCleanFatJet >= 1 '
}

aliases['boosted_nocut'] = {
    'expr': 'PuppiMET_pt > 40 \
            && idxCleanFatJetW != 999 \
            && Alt$(CleanFatJet_pt[idxCleanFatJetW], 0) > 200 \
            && Alt$(CleanFatJet_eta[idxCleanFatJetW], 999) < 2.4'
}

aliases['boosted_fat_jet'] = {
    'expr': 'PuppiMET_pt > 40 \
            && idxCleanFatJetW != 999 \
            && Alt$(CleanFatJet_pt[idxCleanFatJetW], 0) > 200 \
            && FatJet_deepTag_WvsQCD[CleanFatJet_jetIdx[idxCleanFatJetW]] > 0.960 \
            && HvOverFat > 0.4 \
            && Alt$(CleanFatJet_eta[idxCleanFatJetW], 999) < 2.4'
}

aliases['two_jet_res'] ={
    'expr': 'nCleanJet >= 2 \
            && !boosted_fat_jet[0] \
            && HM_Whad_mass > 0 \
            && CleanJet_pt[0] > 30 \
            && PuppiMET_pt[0] > 30 \
            && HM_Hlnjj_MT[0] > 60 \
            && HvOverJJ[0] > 0.4 \
            && CleanJet_pt[1] > 30'
}


aliases['LHEPartWlepPt'] = {
    'linesToAdd': ['.L %s/HWWSemiLepHighMass/LHEPartWlepPt.cc+' % configurations],
    'class': 'LHEPartWlepPt',
    'samples': 'Wjets'
}
data = np.genfromtxt(os.getenv('CMSSW_BASE')+'/src/LatinoAnalysis/Gardener/python/data/ewk/kewk_w.dat', skip_header=2, skip_footer=7)

weight_string = "("
uncert_string = "("
for row in data:
    low  = row[0]
    high = row[1]
    weight = (1+row[2])
    ucert = row[3]

    weight_string+="({}<LHEPartWlepPt[0] && LHEPartWlepPt[0]<={})\
                    *{}+".format(low, high, weight)
    uncert_string+="({}<LHEPartWlepPt[0] && LHEPartWlepPt[0]<={})\
                    *{}+".format(low, high, weight)
# remove trailing + sign and close parentheses
weight_string=weight_string[:-1]+")"
uncert_string=uncert_string[:-1]+")"

aliases['EWK_W_correction'] = {
    'expr': weight_string,
    'samples': 'Wjets'
}
aliases['EWK_W_correction_uncert'] = {
    'expr': uncert_string,
    'samples': 'Wjets'
}




aliases['gstarLow'] = {
    'expr': '( Gen_ZGstar_mass >0 && Gen_ZGstar_mass < 4 )',
    'samples': 'VgS'
}
aliases['gstarHigh'] = {
    'expr': '( Gen_ZGstar_mass <0 || Gen_ZGstar_mass > 4 )',
    'samples': 'VgS'
}



aliases['GenLHE'] = {
'expr': '(Sum$(LHEPart_pdgId == 21) == 0)',
'samples': [x for x in samples if x in ['qqWWqq', 'WW2J'] or 'QQHSBI' in x]
}




# # B-Stuff
vetoThreshold = 20
reqThreshold  = 30
boostedJetBVetoCondition = '(\
CleanJet_pt[CleanJetNotFat_jetIdx] > {threshold} \
&& abs(CleanJet_eta[CleanJetNotFat_jetIdx]) < 2.5 \
)'
resolvedJetBVetoCondition = '(\
HM_idx_j1 >= 0 && HM_idx_j2 >= 0\
&& CleanJet_pt > {threshold} && abs(CleanJet_eta) < 2.5 \
&& CleanJet_jetIdx != CleanJet_jetIdx[HM_idx_j1] \
&& CleanJet_jetIdx != CleanJet_jetIdx[HM_idx_j2] \
)'

bTagBoosted = '(Sum$(Jet_btagDeepB[CleanJet_jetIdx[CleanJetNotFat_jetIdx]] > bWP[0] \
    && {0}) == 0)'.format(boostedJetBVetoCondition)
bTagResolved = '(Sum$(Jet_btagDeepB[CleanJet_jetIdx] > bWP[0] && {0}) == 0)'\
                .format(resolvedJetBVetoCondition)

bTemplate = '((boosted_fat_jet[0]*{0}) || ( two_jet_res[0]*{1}))'.format(bTagBoosted, bTagResolved)

aliases['bVeto'] = {
    'expr': bTemplate.format(threshold=vetoThreshold)
}
aliases['bReq'] = {
    'expr': '!'+bTemplate.format(threshold=reqThreshold)
}

bSF = 'TMath::Exp(Sum$(TMath::Log( \
    {0} * Jet_btagSF_deepcsv_shape[CleanJet_jetIdx] + !{0} * 1 \
    )))'.format('(CleanJet_pt > {threshold} && abs(CleanJet_eta) < 2.5)')

aliases['bVetoSF'] = {
    'expr': bSF.format(threshold=vetoThreshold),
    'samples': mc
}
aliases['bReqSF'] = {
    'expr': bSF.format(threshold=reqThreshold),
    'samples': mc
}

aliases['btagSF'] = {
    'expr': 'bVeto*bVetoSF + bReq*bReqSF + (!bVeto && !bReq)',
    'samples': mc
}

for shift in ['jes','lf','hf','lfstats1','lfstats2','hfstats1','hfstats2','cferr1','cferr2']:

    for targ in ['bVeto', 'bReq']:
        alias = aliases['%sSF%sup' % (targ, shift)] = copy.deepcopy(aliases['%sSF' % targ])
        alias['expr'] = alias['expr'].replace('btagSF_deepcsv_shape', 'btagSF_deepcsv_shape_up_%s' % shift)

        alias = aliases['%sSF%sdown' % (targ, shift)] = copy.deepcopy(aliases['%sSF' % targ])
        alias['expr'] = alias['expr'].replace('btagSF_deepcsv_shape', 'btagSF_deepcsv_shape_down_%s' % shift)


    aliases['btagSF%sup' % shift] = {
        'expr': 'bVeto*bVetoSF{shift}up + bReq*bReqSF{shift}up + (!bVeto && !bReq)'\
                .format(shift = shift),
        'samples': mc
    }
    aliases['btagSF%sdown' % shift] = {
        'expr': 'bVeto*bVetoSF{shift}down + bReq*bReqSF{shift}down + (!bVeto && !bReq)'\
                .format(shift = shift),
        'samples': mc
    }





# https://twiki.cern.ch/twiki/bin/viewauth/CMS/JetWtagging
aliases['WtagSF'] = {
    'expr': '(boostedNoTau21[0] * (1.0*tau21Cut[0] + 0.96*!tau21Cut[0]) + (1-boostedNoTau21[0]))',
    'samples': mc
}
aliases['SFWtagUp'] = {
    'expr': '(boostedNoTau21[0] * (1.06*tau21Cut[0] + 0.89*!tau21Cut[0]) + (1-boostedNoTau21[0]))',
    'samples': mc
}
aliases['SFWtagDown'] = {
    'expr': '(boostedNoTau21[0] * (0.94*tau21Cut[0] + 1.11*!tau21Cut[0]) + (1-boostedNoTau21[0]))',
    'samples': mc
}






aliases['LepWPSF'] = {
    'expr': '((Lepton_isTightElectron_'+eleWP+'[0] > 0.5) * Lepton_tightElectron_'+eleWP+'_TotSF[0] \
    + (Lepton_isTightMuon_'+muWP+'[0] > 0.5)*Lepton_tightMuon_'+muWP+'_TotSF[0])',
    'samples': mc
}
# # variations of tight lepton WP
aliases['SFweightEleUp'] = {
    'expr': '((TMath::Abs(Lepton_pdgId[0]) == 11)*(Lepton_tightElectron_'+eleWP+'_TotSF_Up[0]/Lepton_tightElectron_'+eleWP+'_TotSF[0]) + (TMath::Abs(Lepton_pdgId[0]) == 13))',
    'samples': mc
}
aliases['SFweightEleDown'] = {
    'expr': '((TMath::Abs(Lepton_pdgId[0]) == 11)*(Lepton_tightElectron_'+eleWP+'_TotSF_Down[0]/Lepton_tightElectron_'+eleWP+'_TotSF[0]) + (TMath::Abs(Lepton_pdgId[0]) == 13))',
    'samples': mc
}
aliases['SFweightMuUp'] = {
    'expr': '((TMath::Abs(Lepton_pdgId[0]) == 13)*(Lepton_tightMuon_'+muWP+'_TotSF_Up[0]/Lepton_tightMuon_'+muWP+'_TotSF[0]) + (TMath::Abs(Lepton_pdgId[0]) == 11))',
    'samples': mc
}
aliases['SFweightMuDown'] = {
    'expr': '((TMath::Abs(Lepton_pdgId[0]) == 13)*(Lepton_tightMuon_'+muWP+'_TotSF_Down[0]/Lepton_tightMuon_'+muWP+'_TotSF[0]) + (TMath::Abs(Lepton_pdgId[0]) == 11))',
    'samples': mc
}




# # PU jet Id SF
# puidSFSource = '%s/src/PlotsConfigurations/Configurations/patches/PUID_81XTraining_EffSFandUncties.root' % os.getenv('CMSSW_BASE')

# aliases['PUJetIdSF'] = {
#     'linesToAdd': [
#         'gSystem->AddIncludePath("-I%s/src");' % os.getenv('CMSSW_BASE'),
#         '.L %s/src/PlotsConfigurations/Configurations/patches/pujetidsf_event_new.cc+' % os.getenv('CMSSW_BASE')
#     ],
#     'class': 'PUJetIdEventSF',
#     'args': (puidSFSource, '2016', 'loose'),
#     'samples': mc
# }


aliases['PUJetIdSF'] = {
    'expr' : 'TMath::Exp(Sum$( \
        (Jet_jetId>=2 \
        && ( (Jet_electronIdx1 != Lepton_electronIdx[0]) || Jet_electronIdx1 < 0 )  \
        && ( (Jet_muonIdx1 != Lepton_muonIdx[0] ) || Jet_muonIdx1 < 0 ) \
        )*TMath::Log(Jet_PUIDSF_loose)\
    ))',
  'samples': mc
}




with open(configurations+'/HWWSemiLepHighMass/DeepAK8V2_W_SFs.csv') as csvfile:
    reader = csv.DictReader(row for row in csvfile if not row.startswith('#'))
    deepAK8Dict = dict()
    for row in reader:
        name = '{y}_{ver}_{mtr}_{pT_l}_{pT_h}'.format(
            y    = row['Year'],
            ver  = row['version'],
            mtr  = row['MistaggingRate[%]'],
            pT_l = row['pT_low[GeV]'],
            pT_h = row['pT_high[GeV]']
        )
        deepAK8Dict[name]         = str(row['SF'])
        deepAK8Dict[name+'_up']   = str(float(row['SF'])+float(row['SF_upperErr']))
        deepAK8Dict[name+'_down'] = str(float(row['SF'])+float(row['SF_lowerErr']))
# 200 300
# 300 400
# 400 800
year = '2016'
mtr = '0p5'
aliases['DeepAK8_SF'] = {
    'expr': "( 1 * two_jet_res[0] + !two_jet_res[0]*(" +\
        \
        deepAK8Dict[year+'_Nominal_'+mtr+'_200_300'] +\
        "* (100 < Alt$(CleanFatJet_pt[idxCleanFatJetW],0) \
        && Alt$(CleanFatJet_pt[idxCleanFatJetW],0) < 300)   +" +\
        \
        deepAK8Dict[year+'_Nominal_'+mtr+'_300_400'] +\
        "* (300 < Alt$(CleanFatJet_pt[idxCleanFatJetW],0) \
        && Alt$(CleanFatJet_pt[idxCleanFatJetW],0) < 400)   +" +\
        \
        deepAK8Dict[year+'_Nominal_'+mtr+'_400_800'] +\
        "* (400 < Alt$(CleanFatJet_pt[idxCleanFatJetW],0))   ))",
    'samples': mc
}

aliases['DeepAK8_SF_up'] = {
    'expr': "( 1 * two_jet_res[0] + !two_jet_res[0]*(" +\
        \
        deepAK8Dict[year+'_Nominal_'+mtr+'_200_300_up'] +\
        "* (100 < Alt$(CleanFatJet_pt[idxCleanFatJetW],0) \
        && Alt$(CleanFatJet_pt[idxCleanFatJetW],0) < 300)   +" +\
        \
        deepAK8Dict[year+'_Nominal_'+mtr+'_300_400_up'] +\
        "* (300 < Alt$(CleanFatJet_pt[idxCleanFatJetW],0) \
        && Alt$(CleanFatJet_pt[idxCleanFatJetW],0) < 400)   +" +\
        \
        deepAK8Dict[year+'_Nominal_'+mtr+'_400_800_up'] +\
        "* (400 < Alt$(CleanFatJet_pt[idxCleanFatJetW],0))   ))",
    'samples': mc
}

aliases['DeepAK8_SF_down'] = {
    'expr': "( 1 * two_jet_res[0] + !two_jet_res[0]*(" +\
        \
        deepAK8Dict[year+'_Nominal_'+mtr+'_200_300_down'] +\
        "* (100 < Alt$(CleanFatJet_pt[idxCleanFatJetW],0) \
        && Alt$(CleanFatJet_pt[idxCleanFatJetW],0) < 300)   +" +\
        \
        deepAK8Dict[year+'_Nominal_'+mtr+'_300_400_down'] +\
        "* (300 < Alt$(CleanFatJet_pt[idxCleanFatJetW],0) \
        && Alt$(CleanFatJet_pt[idxCleanFatJetW],0) < 400)   +" +\
        \
        deepAK8Dict[year+'_Nominal_'+mtr+'_400_800_down'] +\
        "* (400 < Alt$(CleanFatJet_pt[idxCleanFatJetW],0))   ))",
    'samples': mc
}





# Fix for single ele trigger eff in 2016

#eleTrigFile = '%s/src/PlotsConfigurations/Configurations/HWWSemiLepHighMass/EleTrigEffAndSF.root' % os.getenv('CMSSW_BASE')

#aliases['EleTrigWeight2016'] = {
#    'linesToAdd': [
#        'gSystem->AddIncludePath("-I%s/src");' % os.getenv('CMSSW_BASE'),
#        '.L %s/src/PlotsConfigurations/Configurations/HWWSemiLepHighMass/weightReader.cc+' % os.getenv('CMSSW_BASE')
#    ],
#    'class': 'WeightReader',
#    'args': (eleTrigFile,'eff_2016BCDEFGH'),
#    'samples': mc
#}

aliases['passSingleElectronHLT']= {
    'expr':'HLT_Ele27_WPTight_Gsf'
}

#aliases['EleTrigSF'] = {
 #   'class': 'WeightReader',
#    'args': (eleTrigFile,'SF_2016BCDEFGH_SF'),
#    'samples': mc
#}

#aliases['trigWeight'] = {
#    'expr' : 'TriggerEffWeight_1l*'+'(Lepton_isTightMuon_'+muWP+'[0]>0.5) +\
#            EleTrigSF*passSingleElectronHLT*(Lepton_isTightElectron_'+eleWP+'[0]>0.5)',
#    'samples':mc
#}





# TODO: choice here between boosted W tagging with tau21 (WtagSF)
#       or DeepAK8 (DeepAK8_SF)
# # data/MC scale factors
aliases['SFweight'] = {
    #'expr': ' * '.join(['puWeight', 'TriggerEffWeight_1l', 'EMTFbug_veto',  'PrefireWeight', 'LepWPSF[0]', 'btagSF[0]', 'PUJetIdSF[0]']),
    'expr': ' * '.join(['puWeight', 'TriggerEffWeight_1l', 'EMTFbug_veto',  'PrefireWeight', 'LepWPSF[0]', 'btagSF[0]', 'PUJetIdSF[0]', 'DeepAK8_SF[0]']),
    #'expr': ' * '.join(['puWeight', 'TriggerEffWeight_1l', 'EMTFbug_veto',  'PrefireWeight', 'LepWPSF[0]', 'btagSF[0]', 'PUJetIdSF[0]', 'WtagSF[0]']),
    #'expr': ' * '.join(['puWeight', 'trigWeight', 'EMTFbug_veto',  'PrefireWeight', 'LepWPSF[0]', 'btagSF[0]', 'PUJetIdSF[0]', 'DeepAK8_SF[0]']),
    'samples': mc
}



# FIXME top stuff
# PostProcessing did not create (anti)topGenPt for ST samples with _ext1
lastcopy = (1 << 13)

aliases['isTTbar'] = {
    'expr': 'Sum$(TMath::Abs(GenPart_pdgId) == 6 && TMath::Odd(GenPart_statusFlags / %d)) == 2' % lastcopy,
    'samples': ['top',]
}
aliases['isSingleTop'] = {
    'expr': 'Sum$(TMath::Abs(GenPart_pdgId) == 6 && TMath::Odd(GenPart_statusFlags / %d)) == 1' % lastcopy,
    'samples': ['top',]
}

aliases['topGenPtOTF'] = {
    'expr': 'Sum$((GenPart_pdgId == 6 && TMath::Odd(GenPart_statusFlags / %d)) * GenPart_pt)' % lastcopy,
    'samples': ['top',]
}
aliases['antitopGenPtOTF'] = {
    'expr': 'Sum$((GenPart_pdgId == -6 && TMath::Odd(GenPart_statusFlags / %d)) * GenPart_pt)' % lastcopy,
    'samples': ['top',]
}




aliases['Top_pTrw'] = {# New Top PAG
    'expr': '(topGenPtOTF * antitopGenPtOTF > 0.) * (TMath::Sqrt((0.103*TMath::Exp(-0.0118*topGenPtOTF) - 0.000134*topGenPtOTF + 0.973) * (0.103*TMath::Exp(-0.0118*antitopGenPtOTF) - 0.000134*antitopGenPtOTF + 0.973))) * (TMath::Sqrt(TMath::Exp(1.61468e-03 + 3.46659e-06*topGenPtOTF - 8.90557e-08*topGenPtOTF*topGenPtOTF) * TMath::Exp(1.61468e-03 + 3.46659e-06*antitopGenPtOTF - 8.90557e-08*antitopGenPtOTF*antitopGenPtOTF))) + (topGenPtOTF * antitopGenPtOTF <= 0.)', # Same Reweighting as other years, but with additional fix for tune CUET -> CP5
    'samples': ['top',]
}


aliases['nCleanGenJet'] = {
    'linesToAdd': ['.L %s/src/PlotsConfigurations/Configurations/Differential/ngenjet.cc+' % os.getenv('CMSSW_BASE')],
    'class': 'CountGenJet',
    'samples': mc
}

##### DY Z pT reweighting
aliases['getGenZpt_OTF'] = {
    'linesToAdd':['.L %s/src/PlotsConfigurations/Configurations/patches/getGenZpt.cc+' % os.getenv('CMSSW_BASE')],
    'class': 'getGenZpt',
    'samples': ['DY']
}
handle = open('%s/src/PlotsConfigurations/Configurations/patches/DYrew30.py' % os.getenv('CMSSW_BASE'),'r')
exec(handle)
handle.close()
aliases['DY_NLO_pTllrw'] = {
    'expr': '('+DYrew['2016']['NLO'].replace('x', 'getGenZpt_OTF')+')*(nCleanGenJet == 0)+1.0*(nCleanGenJet > 0)',
    'samples': ['DY']
}
aliases['DY_LO_pTllrw'] = {
    'expr': '('+DYrew['2016']['LO'].replace('x', 'getGenZpt_OTF')+')*(nCleanGenJet == 0)+1.0*(nCleanGenJet > 0)',
    'samples': ['DY']
}





mc_sbi = [skey for skey in samples if "SBI" in skey]
aliases['CheckforSM'] = {
    'linesToAdd' : [
        'gSystem->Load("libLatinoAnalysisMultiDraw.so")',
        '.L %s/src/PlotsConfigurations/Configurations/HWWSemiLepHighMass/CheckForSM125.cc+' % os.getenv('CMSSW_BASE')
    ],
    'expr': 'CheckforSM()',
    'samples': mc_sbi
}

aliases['SBI_isSMggh'] = {
    'expr': '( abs(Xsec-1.091343e+00) < 1.0e-06 && CheckforSM )', # With protection against "HM" 125 sample
    'samples': mc_sbi
}
aliases['SBI_isSMVBF'] = {
    'expr': '( abs(Xsec-8.496211e-02) < 1.0e-08 && CheckforSM )', # With protection against "HM" 125 sample
    'samples': mc_sbi
}
aliases['SBI_isggWW'] = {
    'expr': '( abs(Xsec-6.387000e-02) < 1.0e-08 )',
    'samples': mc_sbi
}
aliases['SBI_isqqWWqq'] = {
    'expr': '( abs(Xsec-2.160000e+00) < 1.0e-06)',
    'samples': mc_sbi
}
aliases['SBI_isHM'] = {
    'expr': '( !SBI_isSMggh && !SBI_isSMVBF && !SBI_isggWW && !SBI_isqqWWqq )',
    'samples': mc_sbi
}

aliases["nJetHigh2"]={
    'linesToAdd':['.L %s/src/PlotsConfigurations/Configurations/HWWSemiLepHighMass/getNJet.cc+'  % os.getenv('CMSSW_BASE')],
    'class': 'getNJet',
}

aliases["MelaVBFvsGGH_boosted"]={
    'linesToAdd': [
    'gSystem->Load("%s/src/JHUGenMELA/MELA/data/%s/libmcfm_707.so","", kTRUE);'%(os.getenv('CMSSW_BASE'), os.getenv('SCRAM_ARCH')),
    'gSystem->Load("libJHUGenMELAMELA.so","", kTRUE);',
    '.L %s/HWWSemiLepHighMass/MelaGGFvsVBF.cc+' % configurations],
    'class': 'MelaGGFvsVBF',
    'args': (0, "%s/HWWSemiLepHighMass/" % configurations)
}
aliases["MelaVBFvsGGH_resolved"]={
    'linesToAdd': [
    'gSystem->Load("%s/src/JHUGenMELA/MELA/data/%s/libmcfm_707.so","", kTRUE);'%(os.getenv('CMSSW_BASE'), os.getenv('SCRAM_ARCH')),
    'gSystem->Load("libJHUGenMELAMELA.so","", kTRUE);',
    '.L %s/HWWSemiLepHighMass/MelaGGFvsVBF.cc+' % configurations],
    'class': 'MelaGGFvsVBF',
    'args': (1,  "%s/HWWSemiLepHighMass/" % configurations)
}


aliases['kfact'] = { 
    'linesToAdd': [
	'gSystem->Load("%s/src/JHUGenMELA/MELA/data/%s/libmcfm_707.so","", kTRUE);'%(os.getenv('CMSSW_BASE'), os.getenv('SCRAM_ARCH')),
        'gSystem->Load("libJHUGenMELAMELA.so","", kTRUE);',
        'gSystem->AddIncludePath("-I%s/src");' % os.getenv('CMSSW_RELEASE_BASE'),
        '.L %s/src/PlotsConfigurations/Configurations/HWWSemiLepHighMass/kFactorUnc2.cc+' % os.getenv('CMSSW_BASE')
    ],  
    'class': 'kFactorUnc2',
    'args': ('PlotsConfigurations/Configurations/HWWSemiLepHighMass/wjets_kfactor_DH/HT_to_NLO_QCD_k_factors3.root', 'k_factor_2016'),
    'samples': 'Wjets', 
}


#aliases['kfactMjj'] = { 
#    'linesToAdd': [
#        'gSystem->AddIncludePath("-I%s/src");' % os.getenv('CMSSW_RELEASE_BASE'),
#        '.L %s/src/PlotsConfigurations/Configurations/HWWSemiLepHighMass/k_factor_mjj_unc.cc+' % os.getenv('CMSSW_BASE')
#    ],  
#    'class': 'kFactorMjjUnc',
#    #'args': ('PlotsConfigurations/Configurations/monoHWW/SemiLep/Wjets_kfactors/HT_to_NLO_QCD_k_factors_2016_mjj.root', 'k_factor_2016'),
#    'args': ('PlotsConfigurations/Configurations/HWWSemiLepHighMass/wjets_kfactor_DH/HT_to_NLO_QCD_k_factors_mjj.root', 'k_factor_2016'),
#    'samples': 'Wjets', 
#}



#aliases['SBI_isSMggh'] = {
 #   'linesToAdd': ['.L %s/src/PlotsConfigurations/Configurations/HWWSemiLepHighMass/isSample.cc+' % os.getenv('CMSSW_BASE')],
 #   'expr' : 'is_SMggh()',
 #   'samples': mc_sbi
#}
#aliases['SBI_isSMVBF'] = {
#    'linesToAdd': ['.L %s/src/PlotsConfigurations/Configurations/HWWSemiLepHighMass/isSample.cc+' % os.getenv('CMSSW_BASE')],
#    'expr' : 'is_SMVBF()',
#    'samples': mc_sbi
#}
#aliases['SBI_isggWW'] = {
 #   'linesToAdd': ['.L %s/src/PlotsConfigurations/Configurations/HWWSemiLepHighMass/isSample.cc+' % os.getenv('CMSSW_BASE')],
 #   'expr' : 'is_ggWW()',
  #  'samples': mc_sbi
#}
#aliases['SBI_isqqWWqq'] = {
 #   'linesToAdd': ['.L %s/src/PlotsConfigurations/Configurations/HWWSemiLepHighMass/isSample.cc+' % os.getenv('CMSSW_BASE')],
 #   'expr' : 'is_qqWWqq()',
 #   'samples': mc_sbi
#}
#aliases['SBI_isHM'] = {
#    'expr': '( !SBI_isSMggh && !SBI_isSMVBF && !SBI_isggWW && !SBI_isqqWWqq )',
#    'samples': mc_sbi
#}
