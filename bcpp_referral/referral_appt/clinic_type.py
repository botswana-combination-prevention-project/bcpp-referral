from ..referral_code import ReferralCategory


class ClinicTypeError(Exception):
    pass


class ClinicType:
    """Returns the calculated referral appointment date based on
    the referral code and a scheduled appointment date.
    """
    referral_category = ReferralCategory()

    def __init__(self, referral_code=None):
        self.clinic_type = None
        if referral_code in self.referral_category.idcc.all:
            self.clinic_type = 'IDCC'
        elif referral_code in self.referral_category.vct.all:
            self.clinic_type = 'VCT'
        elif referral_code in self.referral_category.anc.all:
            self.clinic_type = 'ANC'
        elif referral_code in self.referral_category.smc.all:
            self.clinic_type = 'SMC'
        else:
            raise ClinicTypeError(f'Unhandled referral code. Got \'{referral_code}\'')

    def __repr__(self):
        return f'{self.__class__.__name__}(referral_code={self.referral_code})'

    def __str__(self):
        return self.clinic_type
