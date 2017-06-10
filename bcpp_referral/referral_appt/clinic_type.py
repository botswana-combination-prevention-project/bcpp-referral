class ClinicTypeError(Exception):
    pass


class ClinicType:
    """Returns the calculated referral appointment date based on
    the referral code and a scheduled appointment date.
    """
    anc_referrals = ['NEG!-PR', 'UNK?-PR', 'POS#-AN']
    idcc_referrals = ['POS!-HI', 'POS!-LO', 'POS#-HI', 'POS#-LO',
                      'POS#NVE', 'POS!NVE', 'POS!-PR', 'POS#-PR', 'POS#-PR',
                      'MASA-CC', 'MASA-DF']
    smc_referrals = ['SMC-NEG', 'SMC-UNK']
    vct_referrals = ['TST-HIV']

    def __init__(self, referral_code=None):
        self.clinic_type = None
        referral_code = referral_code or ''
        if referral_code in self.idcc_referrals:
            self.clinic_type = 'IDCC'
        elif referral_code in self.vct_referrals:
            self.clinic_type = 'VCT'
        elif referral_code in self.anc_referrals:
            self.clinic_type = 'ANC'
        elif referral_code in self.smc_referrals:
            self.clinic_type = 'SMC'
        else:
            raise ClinicTypeError(f'Unhandled referral code. Got {referral_code}')

    def __repr__(self):
        return f'{self.__class__.__name__}(referral_code={self.referral_code})'

    def __str__(self):
        return self.clinic_type
