from edc_constants.constants import MALE, FEMALE, NEG, UNK, POS

from .constants import ON_ART, NAIVE, DEFAULTER, REFERRAL_CODES


class ReferralCodeError(Exception):
    pass


class ReferralCode:

    valid_referral_codes = [
        code for code, _ in REFERRAL_CODES if not code == 'pending']

    def __init__(self, gender=None, circumcised=None, pregnant=None, **kwargs):
        self.gender = gender
        self.pregnant = pregnant
        self.circumcised = circumcised
        self.referral_code = None
        self.subject_status.current.declined
        if (self.subject_status.final_hiv_status == NEG
                and self.subject_status.current.declined):
            self.referral_code = self.referral_code_for_untested
        elif (not self.subject_status.final_hiv_status
                or self.subject_status.final_hiv_status == UNK
                or self.subject_status.current.declined):
            self.referral_code = self.referral_code_for_untested
        else:
            self.referral_code = self.referral_code_for_tested
        if self.referral_code not in self.valid_referral_codes:
            raise ReferralCodeError(
                f'Invalid referral code. Got {self.referral_code}. '
                f'Expected on of {self.valid_referral_codes}')

    @property
    def referral_code_for_untested(self):
        """Returns a referral code or None.
        """
        referral_code = None
        if self.gender == MALE:
            if self.circumcised:
                referral_code = 'TST-HIV'
            else:
                referral_code = 'SMC-UNK'
        elif self.gender == FEMALE:
            if self.pregnant:
                referral_code = 'UNK?-PR'
            else:
                referral_code = 'TST-HIV'
        return referral_code

    @property
    def referral_code_for_tested(self):
        """Returns a referral code or None.
        """
        if self.subject_status.indeterminate:
            referral_code = 'TST-IND'
        elif self.subject_status.final_hiv_status == NEG:
            referral_code = self.referral_code_for_neg
        elif self.subject_status.final_hiv_status == POS:
            referral_code = self.referral_code_for_pos
        else:
            referral_code = 'TST-HIV'
        return referral_code

    @property
    def referral_code_for_neg(self):
        """Returns a referral code or None.
        """
        referral_code = None
        if self.gender == FEMALE and self.pregnant:
            referral_code = 'NEG!-PR'
        elif self.gender == MALE and not self.circumcised:
            referral_code = 'SMC-NEG'
        return referral_code

    @property
    def referral_code_for_pos_naive(self):
        """Returns a referral code or None.
        """
        referral_code = None
        if not self.cd4_result:
            referral_code = 'TST-CD4'
        elif self.cd4_result and self.cd4_result > 500:
            referral_code = 'POS!-HI' if self.subject_status.newly_diagnosed else 'POS#-HI'
        elif self.cd4_result and self.cd4_result <= 500:
            referral_code = 'POS!-LO' if self.subject_status.newly_diagnosed else 'POS#-LO'
        return referral_code

    @property
    def referral_code_for_pos(self):
        referral_code = None
        if (self.gender == FEMALE
                and self.pregnant
                and self.subject_status.final_arv_status == ON_ART):
            referral_code = 'POS#-AN'
        elif (self.gender == FEMALE
              and self.pregnant
              and self.subject_status.final_arv_status == NAIVE):
            referral_code = (
                'POS!-PR' if self.subject_status.newly_diagnosed else 'POS#-PR')
        elif self.subject_status.final_arv_status == NAIVE:
            referral_code = self.referral_code_for_pos_naive
        elif self.subject_status.final_arv_status == ON_ART:
            referral_code = 'MASA-CC'
        elif self.subject_status.final_arv_status == DEFAULTER:
            referral_code = 'MASA-DF'
        return referral_code
