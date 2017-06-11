from ..referral_facility import ReferralFacility, ReferralFacilities

bcpp_referral = ReferralFacilities(name='bcpp')

anc_facility = ReferralFacility(
    name='anc',
    urgent_codes=['NEG!-PR', 'UNK?-PR', 'POS#-AN'],
    routine_codes=[])
idcc_facility = ReferralFacility(
    name='idcc',
    urgent_codes=[
        'POS!-HI', 'POS!-LO', 'POS#-HI', 'POS#-LO',
        'POS#NVE', 'POS!NVE', 'POS!-PR', 'POS#-PR', 'POS#-PR',
        'MASA-DF'],
    routine_codes=['MASA-CC'])

smc_facility = ReferralFacility(
    name='smc',
    urgent_codes=[],
    routine_codes=['SMC-NEG', 'SMC-UNK'])

vct_facility = ReferralFacility(
    name='vct',
    urgent_codes=['TST-HIV'],
    routine_codes=[])

bcpp_referral.add_facility(facility=anc_facility)
bcpp_referral.add_facility(facility=idcc_facility)
bcpp_referral.add_facility(facility=smc_facility)
bcpp_referral.add_facility(facility=vct_facility)
