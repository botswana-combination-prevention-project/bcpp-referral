from edc_constants.constants import MALE, FEMALE, NEG, POS, NAIVE, IND, ON_ART, DEFAULTER


class ReferralCodeError(Exception):
    pass


class ReferralCodeTested:
    """Sets a referral code for a tested MALE considering
    their circumcision status or a FEMALE considering their
    pregnancy status in addition to ARV status, etc.
    """

    def __init__(self, gender=None, circumcised=None, pregnant=None,
                 hiv_status=None, newly_diagnosed=None, arv_status=None,
                 cd4_result=None):
        self.referral_code = None
        self.arv_status = arv_status
        self.cd4_result = cd4_result
        self.circumcised = circumcised
        self.gender = gender
        self.hiv_status = hiv_status
        self.newly_diagnosed = newly_diagnosed
        self.pregnant = pregnant
        if hiv_status == NEG:
            self.referral_code = self._referral_code_for_neg
        elif hiv_status == POS:
            self.referral_code = self._referral_code_for_pos
        elif self.hiv_status == IND:
            self.referral_code = 'TST-IND'
        else:
            raise ReferralCodeError(
                f'Unable to determine the referral code. Got {repr(self)}.')

        if self.newly_diagnosed:
            self.referral_code = self.referral_code.replace('#', '!')

    def __repr__(self):
        return f'{self.__class__.__name__}({self.__dict__})'

    @property
    def _referral_code_for_neg(self):
        """Returns a referral code or None.
        """
        referral_code = None
        if self.gender == FEMALE and self.pregnant:
            referral_code = 'NEG!-PR'
        elif self.gender == MALE and not self.circumcised:
            referral_code = 'SMC-NEG'
        else:
            raise ReferralCodeError(
                f'Unable to determine the referral code. Got {repr(self)}.')
        return referral_code

    @property
    def _referral_code_for_pos_naive(self):
        """Returns a referral code or None.
        """
        referral_code = None
        if not self.cd4_result:
            referral_code = 'POS#NVE'
        elif 0 <= self.cd4_result <= 500:
            referral_code = 'POS#-LO'
        elif self.cd4_result > 500:
            referral_code = 'POS#-HI'
        else:
            raise ReferralCodeError(
                f'Unable to determine the referral code. Got {repr(self)}.')
        return referral_code

    @property
    def _referral_code_for_pos(self):
        referral_code = None
        if self.pregnant and self.arv_status == ON_ART:
            referral_code = 'POS#-AN'
        elif self.pregnant and self.arv_status == NAIVE:
            referral_code = 'POS#-PR'
        elif self.arv_status in [None, NAIVE]:
            referral_code = self._referral_code_for_pos_naive
        elif self.arv_status == ON_ART:
            referral_code = 'MASA-CC'
        elif self.arv_status == DEFAULTER:
            referral_code = 'MASA-DF'
        else:
            raise ReferralCodeError(
                f'Unable to determine the referral code. Got {repr(self)}.')
        return referral_code
