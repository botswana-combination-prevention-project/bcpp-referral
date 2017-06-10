from edc_constants.constants import MALE, FEMALE, NEG, UNK, POS, NAIVE, IND

from bcpp_status.constants import ON_ART, DEFAULTER

from .choices import REFERRAL_CODES


class ReferralCodeError(Exception):
    pass


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


class ReferralCode:

    referral_code_untested_cls = ReferralCodeUntested
    referral_code_tested_cls = ReferralCodeTested
    valid_hiv_status = [POS, NEG, IND, UNK, None]
    valid_arv_status = [NAIVE, ON_ART, DEFAULTER, None]
    valid_referral_codes = [
        code for code, _ in REFERRAL_CODES if not code == 'pending']

    def __init__(self, gender=None, circumcised=None, pregnant=None,
                 status_helper=None, cd4_result=None, **kwargs):
        self.referral_code = None
        if status_helper.final_hiv_status not in self.valid_hiv_status:
            raise ReferralCodeError(
                f'Invalid HIV status. Got {status_helper.final_hiv_status}. '
                f'Expected one of {self.valid_hiv_status}.')
        elif status_helper.final_arv_status not in self.valid_arv_status:
            raise ReferralCodeError(
                f'Invalid ARV status. Got {status_helper.final_arv_status}. '
                f'Expected one of {self.valid_arv_status}.')
        elif (status_helper.final_hiv_status in [None, UNK]
              or status_helper.current.declined):
            obj = self.referral_code_untested_cls(
                gender=gender, circumcised=circumcised, pregnant=pregnant)
            self.referral_code = obj.referral_code

        else:
            obj = self.referral_code_tested_cls(
                gender=gender,
                circumcised=circumcised,
                pregnant=pregnant,
                hiv_status=status_helper.final_hiv_status,
                arv_status=status_helper.final_arv_status,
                newly_diagnosed=status_helper.newly_diagnosed,
                cd4_result=cd4_result)
            self.referral_code = obj.referral_code
