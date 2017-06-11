from edc_constants.constants import NEG, UNK, POS, NAIVE, IND

from bcpp_status.constants import ON_ART, DEFAULTER

from ..choices import REFERRAL_CODES
from .referral_code_tested import ReferralCodeError, ReferralCodeTested
from .referral_code_untested import ReferralCodeUntested


class ReferralCode:

    """A class to determine the referral code based on criteria
    such as gender, hiv_status, arv_status, circumcision,
    pregnancy, etc.
    """

    referral_code_untested_cls = ReferralCodeUntested
    referral_code_tested_cls = ReferralCodeTested
    valid_hiv_status = [POS, NEG, IND, UNK, None]
    valid_arv_status = [NAIVE, ON_ART, DEFAULTER, None]
    valid_referral_codes = [
        code for code, _ in REFERRAL_CODES if not code == 'pending']

    def __init__(self, gender=None, circumcised=None, pregnant=None,
                 final_hiv_status=None, final_arv_status=None,
                 newly_diagnosed=None, declined=None, cd4_result=None, **kwargs):

        self.referral_code = None

        if final_hiv_status not in self.valid_hiv_status:
            raise ReferralCodeError(
                f'Invalid HIV status. Got {final_hiv_status}. '
                f'Expected one of {self.valid_hiv_status}.')
        elif final_arv_status not in self.valid_arv_status:
            raise ReferralCodeError(
                f'Invalid ARV status. Got {final_arv_status}. '
                f'Expected one of {self.valid_arv_status}.')
        elif (final_hiv_status in [None, UNK] or declined):
            obj = self.referral_code_untested_cls(
                gender=gender, circumcised=circumcised, pregnant=pregnant)
            self.referral_code = obj.referral_code

        else:
            obj = self.referral_code_tested_cls(
                gender=gender,
                circumcised=circumcised,
                pregnant=pregnant,
                hiv_status=final_hiv_status,
                arv_status=final_arv_status,
                newly_diagnosed=newly_diagnosed,
                cd4_result=cd4_result)
            self.referral_code = obj.referral_code
