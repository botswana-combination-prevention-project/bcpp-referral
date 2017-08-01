from django.test import TestCase, tag

from edc_constants.constants import POS, MALE, NAIVE, NEG, FEMALE, UNK
from edc_constants.constants import IND, ON_ART, DEFAULTER

from ..referral_code import ReferralCode, ReferralCodeError
from ..referral_code import ReferralCodeUntested, ReferralCodeTested


class TestReferralCodeUntested(TestCase):

    def test_referral_code_untested(self):
        code = ReferralCodeUntested()
        self.assertIsNone(code.referral_code)

    def test_referral_code_untested_repr(self):
        code = ReferralCodeUntested()
        self.assertTrue(repr(code))

    def test_referral_code(self):
        code = ReferralCode()
        self.assertIsNone(code.referral_code)

    def test_referral_invalid_hiv_status(self):
        self.assertRaises(
            ReferralCodeError,
            ReferralCode, final_hiv_status='BLAH')

    def test_referral_invalid_arv_status(self):
        self.assertRaises(
            ReferralCodeError,
            ReferralCode, final_arv_status='BLAH')

    def test_referral_hivnone(self):
        code = ReferralCode(final_hiv_status=None, gender=FEMALE)
        self.assertEqual(code.referral_code, 'TST-HIV')

    def test_referral_hivind(self):
        for gender in [MALE, FEMALE]:
            with self.subTest(gender=gender):
                code = ReferralCode(final_hiv_status=IND, gender=gender)
                self.assertEqual(code.referral_code, 'TST-IND')

    def test_referral_code_hivpos_on_art(self):
        code = ReferralCode(
            final_hiv_status=POS, final_arv_status=ON_ART)
        self.assertEqual(code.referral_code, 'MASA-CC')

    def test_referral_code_hivpos_defaulter(self):
        code = ReferralCode(final_hiv_status=POS, final_arv_status=DEFAULTER)
        self.assertEqual(code.referral_code, 'MASA-DF')

    def test_referral_code_male_hivunknown_uncircumcised(self):
        for final_hiv_status in [UNK, None]:
            with self.subTest(final_hiv_status=final_hiv_status):
                for circumcised in [None, False]:
                    with self.subTest(circumcised=circumcised):
                        code = ReferralCode(
                            final_hiv_status=final_hiv_status, declined=False,
                            gender=MALE, circumcised=circumcised)
                        self.assertEqual(code.referral_code, 'SMC-UNK')

    def test_referral_code_male_declined(self):
        """Asserts male NEG/UNK who declines and not circumcised/UNKNOWN
        returns 'SMC-UNK'.
        """
        for final_hiv_status in [NEG, UNK, None]:
            with self.subTest(final_hiv_status=final_hiv_status):
                for circumcised in [None, False]:
                    with self.subTest(circumcised=circumcised):
                        code = ReferralCode(
                            final_hiv_status=final_hiv_status, declined=True,
                            gender=MALE, circumcised=circumcised)
                        self.assertEqual(code.referral_code, 'SMC-UNK')

    def test_referral_code_male_declined_circumcised(self):
        code = ReferralCode(final_hiv_status=NEG, declined=True,
                            gender=MALE, circumcised=True)
        self.assertEqual(code.referral_code, 'TST-HIV')

    def test_referral_code_female_declined_not_pregnant(self):
        """Asserts female NEG/UNK who declines and not pregnant/UNKNOWN
        returns 'TST-HIV'.
        """
        for final_hiv_status in [NEG, UNK]:
            with self.subTest(final_hiv_status=final_hiv_status):
                for pregnant in [None, False]:
                    with self.subTest(pregnant=pregnant):
                        code = ReferralCode(
                            final_hiv_status=final_hiv_status, declined=True,
                            gender=FEMALE, pregnant=pregnant)
                        self.assertEqual(code.referral_code, 'TST-HIV')

    def test_referral_code_female_hivneg_pregnant(self):
        code = ReferralCode(final_hiv_status=NEG,
                            gender=FEMALE, pregnant=True)
        self.assertEqual(code.referral_code, 'NEG!-PR')

    def test_referral_code_female_hivunknown_pregnant(self):
        code = ReferralCode(
            final_hiv_status=UNK,
            gender=FEMALE, pregnant=True)
        self.assertEqual(code.referral_code, 'UNK?-PR')

    def test_referral_code_female_hivunknown_declined_pregnant(self):
        code = ReferralCode(final_hiv_status=UNK, declined=True,
                            gender=FEMALE, pregnant=True)
        self.assertEqual(code.referral_code, 'UNK?-PR')

    def test_referral_code_hivneg_uncircumcised(self):
        for circumcised in [None, False]:
            with self.subTest(circumcised=circumcised):
                code = ReferralCode(final_hiv_status=NEG,
                                    gender=MALE, circumcised=circumcised)
                self.assertEqual(code.referral_code, 'SMC-NEG')


@tag('referral_code')
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


@tag('referral_code')
class TestReferralCodePosFemale(TestCase):

    def test_referral_code_knownpos_onart_not_pregnant(self):
        for newly_diagnosed in [True, False, None]:
            with self.subTest(newly_diagnosed=newly_diagnosed):
                for pregnant in [None, False]:
                    with self.subTest(pregnant=pregnant):
                        code = ReferralCode(
                            final_hiv_status=POS,
                            final_arv_status=ON_ART,
                            newly_diagnosed=newly_diagnosed,
                            gender=FEMALE, pregnant=pregnant)
                        self.assertEqual(code.referral_code, 'MASA-CC')

    def test_referral_code_newpos_naive_not_pregnant(self):
        for pregnant in [None, False]:
            with self.subTest(pregnant=pregnant):
                code = ReferralCode(
                    final_hiv_status=POS, final_arv_status=NAIVE,
                    newly_diagnosed=True,
                    gender=FEMALE, pregnant=pregnant)
                self.assertEqual(code.referral_code, 'POS!NVE')

    def test_referral_code_knownpos_naive(self):
        for newly_diagnosed in [None, False]:
            with self.subTest(newly_diagnosed=newly_diagnosed):
                for pregnant in [None, False]:
                    with self.subTest(pregnant=pregnant):
                        code = ReferralCode(
                            final_hiv_status=POS,
                            final_arv_status=NAIVE,
                            newly_diagnosed=newly_diagnosed,
                            gender=FEMALE, pregnant=pregnant)
                        self.assertEqual(code.referral_code, 'POS#NVE')

    def test_referral_code_newpos_naive_preg(self):
        code = ReferralCode(
            final_hiv_status=POS,
            final_arv_status=NAIVE,
            newly_diagnosed=True,
            gender=FEMALE, pregnant=True)
        self.assertEqual(code.referral_code, 'POS!-PR')

    def test_referral_code_pos_naive_preg(self):
        code = ReferralCode(
            final_hiv_status=POS, final_arv_status=NAIVE,
            gender=FEMALE, pregnant=True)
        self.assertEqual(code.referral_code, 'POS#-PR')

    def test_referral_code_pos_onart_preg(self):
        code = ReferralCode(
            final_hiv_status=POS, final_arv_status=ON_ART,
            gender=FEMALE, pregnant=True)
        self.assertEqual(code.referral_code, 'POS#-AN')


@tag('referral_code')
class TestReferralCodePosMale(TestCase):

    def test_referral_code_hivpos(self):
        code = ReferralCode(final_hiv_status=POS, gender=MALE)
        self.assertEqual(code.referral_code, 'POS#NVE')

    def test_referral_code_hivpos_circumcised(self):
        code = ReferralCode(final_hiv_status=POS,
                            gender=MALE, circumcised=True)
        self.assertEqual(code.referral_code, 'POS#NVE')

    def test_referral_code_male_knownpos_onart(self):
        for circumcised in [None, False, True]:
            with self.subTest(circumcised=circumcised):
                code = ReferralCode(
                    final_hiv_status=POS, final_arv_status=ON_ART,
                    gender=MALE, circumcised=circumcised)
                self.assertEqual(code.referral_code, 'MASA-CC')

    def test_referral_code_male_pos_naive(self):
        for circumcised in [None, False, True]:
            with self.subTest(circumcised=circumcised):
                code = ReferralCode(
                    final_hiv_status=POS, final_arv_status=NAIVE,
                    gender=MALE, circumcised=circumcised)
                self.assertEqual(code.referral_code, 'POS#NVE')

    def test_referral_code_male_newpos_naive(self):
        for circumcised in [None, False, True]:
            with self.subTest(circumcised=circumcised):
                code = ReferralCode(
                    final_hiv_status=POS, final_arv_status=NAIVE,
                    newly_diagnosed=True,
                    gender=MALE, circumcised=circumcised)
                self.assertEqual(code.referral_code, 'POS!NVE')


@tag('referral_code')
class TestReferralCodePosCd4(TestCase):

    def test_referral_code_hivpos_lo_cd4(self):
        code = ReferralCode(final_hiv_status=POS,
                            gender=MALE, cd4_result=100)
        self.assertEqual(code.referral_code, 'POS#-LO')

    def test_referral_code_hivpos_hi_cd4(self):
        code = ReferralCode(
            final_hiv_status=POS,
            gender=MALE, circumcised=True, cd4_result=600)
        self.assertEqual(code.referral_code, 'POS#-HI')

    def test_referral_code_hivpos_invalid_cd4(self):
        self.assertRaises(
            ReferralCodeError,
            ReferralCode, final_hiv_status=POS,
            gender=MALE, circumcised=True, cd4_result=-1)
