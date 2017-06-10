from ..referral_code import ReferralCategory

bcpp_referral_category = ReferralCategory(name='bcpp')

bcpp_referral_category.add(
    name='anc',
    urgent_referral_codes=['NEG!-PR', 'UNK?-PR', 'POS#-AN'],
    routine_referral_codes=[])

bcpp_referral_category.add(
    name='idcc',
    urgent_referral_codes=[
        'POS!-HI', 'POS!-LO', 'POS#-HI', 'POS#-LO',
        'POS#NVE', 'POS!NVE', 'POS!-PR', 'POS#-PR', 'POS#-PR',
        'MASA-DF'],
    routine_referral_codes=['MASA-CC'])

bcpp_referral_category.add(
    name='smc',
    urgent_referral_codes=[],
    routine_referral_codes=['SMC-NEG', 'SMC-UNK'])

bcpp_referral_category.add(
    name='vct',
    urgent_referral_codes=['TST-HIV'],
    routine_referral_codes=[])
