from django.test import TestCase, tag

from edc_constants.constants import POS, MALE, NAIVE, NEG, FEMALE, UNK, IND

from ..referral_code import ReferralCode, ReferralCodeError
from bcpp_status.constants import ON_ART, DEFAULTER
from bcpp_referral.referral_code import ReferralCodeUntested,\
    ReferralCodeTested


class MockCurrent:

    def __init__(self, declined=None, **kwargs):
        self.declined = declined

    def __repr__(self):
        return f'{self.__class__.__name__}({self.__dict__})'


class MockStatusHelper:

    def __init__(self, final_hiv_status=None, final_arv_status=None,
                 indeterminate=None, declined=None, newly_diagnosed=None):
        self.current = MockCurrent(declined=declined)
        self.final_hiv_status = final_hiv_status
        self.final_arv_status = final_arv_status
        self.indeterminate = indeterminate
        self.newly_diagnosed = newly_diagnosed

    def __repr__(self):
        return f'{self.__class__.__name__}({self.__dict__})'


class TestReferralCodeUntested(TestCase):

    def test_referral_code_untested(self):
        code = ReferralCodeUntested()
        self.assertIsNone(code.referral_code)

    def test_referral_code_untested_repr(self):
        code = ReferralCodeUntested()
        self.assertTrue(repr(code))

    def test_referral_code(self):
        status_helper = MockStatusHelper()
        code = ReferralCode(status_helper=status_helper)
        self.assertIsNone(code.referral_code)

    def test_referral_invalid_hiv_status(self):
        status_helper = MockStatusHelper(final_hiv_status='BLAH')
        self.assertRaises(
            ReferralCodeError,
            ReferralCode, status_helper=status_helper)

    def test_referral_invalid_arv_status(self):
        status_helper = MockStatusHelper(final_arv_status='BLAH')
        self.assertRaises(
            ReferralCodeError,
            ReferralCode, status_helper=status_helper)

    def test_referral_hivnone(self):
        status_helper = MockStatusHelper(final_hiv_status=None)
        code = ReferralCode(status_helper=status_helper, gender=FEMALE)
        self.assertEqual(code.referral_code, 'TST-HIV')

    def test_referral_hivind(self):
        status_helper = MockStatusHelper(final_hiv_status=IND)
        for gender in [MALE, FEMALE]:
            with self.subTest(gender=gender):
                code = ReferralCode(status_helper=status_helper, gender=gender)
                self.assertEqual(code.referral_code, 'TST-IND')

    def test_referral_code_hivpos_on_art(self):
        status_helper = MockStatusHelper(
            final_hiv_status=POS, final_arv_status=ON_ART)
        code = ReferralCode(status_helper=status_helper)
        self.assertEqual(code.referral_code, 'MASA-CC')

    def test_referral_code_hivpos_defaulter(self):
        status_helper = MockStatusHelper(
            final_hiv_status=POS, final_arv_status=DEFAULTER)
        code = ReferralCode(status_helper=status_helper)
        self.assertEqual(code.referral_code, 'MASA-DF')

    def test_referral_code_male_hivunknown_uncircumcised(self):
        for final_hiv_status in [UNK, None]:
            with self.subTest(final_hiv_status=final_hiv_status):
                status_helper = MockStatusHelper(
                    final_hiv_status=final_hiv_status, declined=False)
                for circumcised in [None, False]:
                    with self.subTest(circumcised=circumcised):
                        code = ReferralCode(status_helper=status_helper,
                                            gender=MALE, circumcised=circumcised)
                        self.assertEqual(code.referral_code, 'SMC-UNK')

    def test_referral_code_male_declined(self):
        """Asserts male NEG/UNK who declines and not circumcised/UNKNOWN
        returns 'SMC-UNK'.
        """
        for final_hiv_status in [NEG, UNK, None]:
            with self.subTest(final_hiv_status=final_hiv_status):
                status_helper = MockStatusHelper(
                    final_hiv_status=final_hiv_status, declined=True)
                for circumcised in [None, False]:
                    with self.subTest(circumcised=circumcised):
                        code = ReferralCode(status_helper=status_helper,
                                            gender=MALE, circumcised=circumcised)
                        self.assertEqual(code.referral_code, 'SMC-UNK')

    def test_referral_code_male_declined_circumcised(self):
        status_helper = MockStatusHelper(final_hiv_status=NEG, declined=True)
        code = ReferralCode(status_helper=status_helper,
                            gender=MALE, circumcised=True)
        self.assertEqual(code.referral_code, 'TST-HIV')

    def test_referral_code_female_declined_not_pregnant(self):
        """Asserts female NEG/UNK who declines and not pregnant/UNKNOWN
        returns 'TST-HIV'.
        """
        for final_hiv_status in [NEG, UNK]:
            with self.subTest(final_hiv_status=final_hiv_status):
                status_helper = MockStatusHelper(
                    final_hiv_status=final_hiv_status, declined=True)
                for pregnant in [None, False]:
                    with self.subTest(pregnant=pregnant):
                        code = ReferralCode(status_helper=status_helper,
                                            gender=FEMALE, pregnant=pregnant)
                        self.assertEqual(code.referral_code, 'TST-HIV')

    def test_referral_code_female_hivneg_pregnant(self):
        status_helper = MockStatusHelper(final_hiv_status=NEG)
        code = ReferralCode(status_helper=status_helper,
                            gender=FEMALE, pregnant=True)
        self.assertEqual(code.referral_code, 'NEG!-PR')

    def test_referral_code_female_hivunknown_pregnant(self):
        status_helper = MockStatusHelper(final_hiv_status=UNK)
        code = ReferralCode(status_helper=status_helper,
                            gender=FEMALE, pregnant=True)
        self.assertEqual(code.referral_code, 'UNK?-PR')

    def test_referral_code_female_hivunknown_declined_pregnant(self):
        status_helper = MockStatusHelper(final_hiv_status=UNK, declined=True)
        code = ReferralCode(status_helper=status_helper,
                            gender=FEMALE, pregnant=True)
        self.assertEqual(code.referral_code, 'UNK?-PR')

    def test_referral_code_hivneg_uncircumcised(self):
        status_helper = MockStatusHelper(final_hiv_status=NEG)
        for circumcised in [None, False]:
            with self.subTest(circumcised=circumcised):
                code = ReferralCode(status_helper=status_helper,
                                    gender=MALE, circumcised=circumcised)
                self.assertEqual(code.referral_code, 'SMC-NEG')


class TestReferralCodeTested(TestCase):

    def test_referral_code_tested(self):
        self.assertRaises(
            ReferralCodeError,
            ReferralCodeTested)

    def test_referral_code_tested_pos_repr(self):
        code = ReferralCodeTested(hiv_status=POS, gender=MALE)
        self.assertTrue(repr(code))

    def test_referral_code_requires_gender(self):
        """Asserts NEG, None without gender raises, POS, IND does not.
        """
        for hiv_status in [NEG, None]:
            with self.subTest(hiv_status=hiv_status):
                self.assertRaises(
                    ReferralCodeError,
                    ReferralCodeTested, hiv_status=hiv_status)
        for hiv_status in [POS, IND]:
            with self.subTest(hiv_status=hiv_status):
                obj = ReferralCodeTested(hiv_status=hiv_status)
                self.assertIsNotNone(obj.referral_code)

    def test_referral_code_invalid_art(self):
        self.assertRaises(
            ReferralCodeError,
            ReferralCodeTested, hiv_status=POS, arv_status='BLAH')


class TestReferralCodePosFemale(TestCase):

    def test_referral_code_knownpos_onart_not_pregnant(self):
        for newly_diagnosed in [True, False, None]:
            with self.subTest(newly_diagnosed=newly_diagnosed):
                status_helper = MockStatusHelper(
                    final_hiv_status=POS,
                    final_arv_status=ON_ART,
                    newly_diagnosed=newly_diagnosed)
                for pregnant in [None, False]:
                    with self.subTest(pregnant=pregnant):
                        code = ReferralCode(
                            status_helper=status_helper,
                            gender=FEMALE, pregnant=pregnant)
                        self.assertEqual(code.referral_code, 'MASA-CC')

    def test_referral_code_newpos_naive_not_pregnant(self):
        status_helper = MockStatusHelper(
            final_hiv_status=POS, final_arv_status=NAIVE, newly_diagnosed=True)
        for pregnant in [None, False]:
            with self.subTest(pregnant=pregnant):
                code = ReferralCode(status_helper=status_helper,
                                    gender=FEMALE, pregnant=pregnant)
                self.assertEqual(code.referral_code, 'POS!NVE')

    def test_referral_code_knownpos_naive(self):
        for newly_diagnosed in [None, False]:
            with self.subTest(newly_diagnosed=newly_diagnosed):
                status_helper = MockStatusHelper(
                    final_hiv_status=POS,
                    final_arv_status=NAIVE,
                    newly_diagnosed=newly_diagnosed)
                for pregnant in [None, False]:
                    with self.subTest(pregnant=pregnant):
                        code = ReferralCode(
                            status_helper=status_helper,
                            gender=FEMALE, pregnant=pregnant)
                        self.assertEqual(code.referral_code, 'POS#NVE')

    def test_referral_code_newpos_naive_preg(self):
        status_helper = MockStatusHelper(
            final_hiv_status=POS, final_arv_status=NAIVE, newly_diagnosed=True)
        code = ReferralCode(
            status_helper=status_helper,
            gender=FEMALE, pregnant=True)
        self.assertEqual(code.referral_code, 'POS!-PR')

    def test_referral_code_pos_naive_preg(self):
        status_helper = MockStatusHelper(
            final_hiv_status=POS, final_arv_status=NAIVE)
        code = ReferralCode(status_helper=status_helper,
                            gender=FEMALE, pregnant=True)
        self.assertEqual(code.referral_code, 'POS#-PR')

    def test_referral_code_pos_onart_preg(self):
        status_helper = MockStatusHelper(
            final_hiv_status=POS, final_arv_status=ON_ART)
        code = ReferralCode(status_helper=status_helper,
                            gender=FEMALE, pregnant=True)
        self.assertEqual(code.referral_code, 'POS#-AN')


class TestReferralCodePosMale(TestCase):

    def test_referral_code_hivpos(self):
        status_helper = MockStatusHelper(final_hiv_status=POS)
        code = ReferralCode(status_helper=status_helper, gender=MALE)
        self.assertEqual(code.referral_code, 'POS#NVE')

    def test_referral_code_hivpos_circumcised(self):
        status_helper = MockStatusHelper(final_hiv_status=POS)
        code = ReferralCode(status_helper=status_helper,
                            gender=MALE, circumcised=True)
        self.assertEqual(code.referral_code, 'POS#NVE')

    def test_referral_code_male_knownpos_onart(self):
        status_helper = MockStatusHelper(
            final_hiv_status=POS, final_arv_status=ON_ART)
        for circumcised in [None, False, True]:
            with self.subTest(circumcised=circumcised):
                code = ReferralCode(status_helper=status_helper,
                                    gender=MALE, circumcised=circumcised)
                self.assertEqual(code.referral_code, 'MASA-CC')

    def test_referral_code_male_pos_naive(self):
        status_helper = MockStatusHelper(
            final_hiv_status=POS, final_arv_status=NAIVE)
        for circumcised in [None, False, True]:
            with self.subTest(circumcised=circumcised):
                code = ReferralCode(status_helper=status_helper,
                                    gender=MALE, circumcised=circumcised)
                self.assertEqual(code.referral_code, 'POS#NVE')

    def test_referral_code_male_newpos_naive(self):
        status_helper = MockStatusHelper(
            final_hiv_status=POS, final_arv_status=NAIVE, newly_diagnosed=True)
        for circumcised in [None, False, True]:
            with self.subTest(circumcised=circumcised):
                code = ReferralCode(
                    status_helper=status_helper,
                    gender=MALE, circumcised=circumcised)
                self.assertEqual(code.referral_code, 'POS!NVE')


class TestReferralCodePosCd4(TestCase):

    def test_referral_code_hivpos_lo_cd4(self):
        status_helper = MockStatusHelper(final_hiv_status=POS)
        code = ReferralCode(status_helper=status_helper,
                            gender=MALE, cd4_result=100)
        self.assertEqual(code.referral_code, 'POS#-LO')

    def test_referral_code_hivpos_hi_cd4(self):
        status_helper = MockStatusHelper(final_hiv_status=POS)
        code = ReferralCode(status_helper=status_helper,
                            gender=MALE, circumcised=True, cd4_result=600)
        self.assertEqual(code.referral_code, 'POS#-HI')

    def test_referral_code_hivpos_invalid_cd4(self):
        status_helper = MockStatusHelper(final_hiv_status=POS)
        self.assertRaises(
            ReferralCodeError,
            ReferralCode, status_helper=status_helper,
            gender=MALE, circumcised=True, cd4_result=-1)
