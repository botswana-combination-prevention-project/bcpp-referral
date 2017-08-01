from edc_constants.constants import MALE, FEMALE


class ReferralCodeUntested:
    """Sets a referral code for an untested MALE considering
    their circumcision status or a FEMALE considering their
    pregnancy status.
    """

    def __init__(self, gender=None, circumcised=None, pregnant=None):

        self.referral_code = None
        if gender == MALE:
            if circumcised:
                self.referral_code = 'TST-HIV'
            else:
                self.referral_code = 'SMC-UNK'
        elif gender == FEMALE:
            if pregnant:
                self.referral_code = 'UNK?-PR'
            else:
                self.referral_code = 'TST-HIV'

    def __repr__(self):
        return f'{self.__class__.__name__}({self.__dict__})'
