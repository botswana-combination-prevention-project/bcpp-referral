# bcpp-referral

[![Build Status](https://travis-ci.org/botswana-harvard/bcpp-referral.svg?branch=develop)](https://travis-ci.org/botswana-harvard/bcpp-referral) [![Coverage Status](https://coveralls.io/repos/github/botswana-harvard/bcpp-referral/badge.svg?branch=develop)](https://coveralls.io/github/botswana-harvard/bcpp-referral?branch=develop)

collate and distribute referral data for BCPP


## Create the referral facilities in the location:

Associate each facility with a unique list of referral codes. Separate the referral code lists into `urgent_codes` and `routine_codes`. In addition to its own parameters, `ReferralFacility` accepts the parameters of `edc_appointment.facility`.

    from ..referral_facility import ReferralFacility
    
    anc_facility = ReferralFacility(
        name='anc',
        urgent_codes=['NEG!-PR', 'UNK?-PR', 'POS#-AN'],
        routine_codes=[],
        days=[TU, WE], forward_only=True)
    
    idcc_facility = ReferralFacility(
        name='idcc',
        urgent_codes=[
            'POS!-HI', 'POS!-LO', 'POS#-HI', 'POS#-LO',
            'POS#NVE', 'POS!NVE', 'POS!-PR', 'POS#-PR', 'POS#-PR',
            'MASA-DF'],
        routine_codes=['MASA-CC'],
        days=[MO, TU, WE, TH, FR], forward_only=True)
    
    smc_facility = ReferralFacility(
        name='smc',
        urgent_codes=[],
        routine_codes=['SMC-NEG', 'SMC-UNK'],
        days=[TH], forward_only=True)
    
    vct_facility = ReferralFacility(
        name='vct',
        urgent_codes=['TST-HIV'],
        routine_codes=[]
        days=[MO, TU, WE, TH, FR], forward_only=True)
    
    
## Create the collection of referral facilities for a location and add each facility:
    
    from ..referral_facility import ReferralFacilities
    
    referral_facilities = ReferralFacilities(name='mochudi')
    
    referral_facilities.add_facility(facility=anc_facility)
    referral_facilities.add_facility(facility=idcc_facility)
    referral_facilities.add_facility(facility=smc_facility)
    referral_facilities.add_facility(facility=vct_facility)

    
## Refer a participant:

    from bcpp_status import StatusHelper

    data_helper = DataHelper(subject_visit=subject_visit)
    status_helper = StatusHelper(subject_visit=subject_visit)
    data = {}
    data.update(**data_helper.data)
    data.update(**status_helper.__dict__)
    referral = Referral(referral_facilities=self.facilities, **data)
    
    >>> referral.subject_identifier
    '1234567'

    >>> referral.referral_code
    POS#NVE

    >>> referral.referral_appt_datetime
    datetime.datetime(2017, 6, 13, 19, 54, 27, 948269, tzinfo=tzutc())

    >>> referral.urgent_referral
    True

    
    
    

    