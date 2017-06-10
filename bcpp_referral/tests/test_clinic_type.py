from django.test import TestCase, tag

from ..referral_appt import ClinicType


class TestClinicType(TestCase):

    def test_clinic_type_idcc(self):
        for referral_code in [
            'POS!-PR', 'POS#-PR', 'MASA-CC', 'POS!-HI',
                'POS!-LO', 'POS#-HI', 'POS#-LO', 'POS#NVE', 'POS!NVE']:
            with self.subTest(referral_code=referral_code):
                obj = ClinicType(referral_code=referral_code)
                self.assertEqual(str(obj), 'IDCC')

    def test_clinic_type_vct(self):
        for referral_code in ['TST-HIV']:
            with self.subTest(referral_code=referral_code):
                obj = ClinicType(referral_code=referral_code)
                self.assertEqual(str(obj), 'VCT')

    def test_clinic_type_anc(self):
        for referral_code in ['NEG!-PR', 'UNK?-PR', 'POS#-AN']:
            with self.subTest(referral_code=referral_code):
                obj = ClinicType(referral_code=referral_code)
                self.assertEqual(str(obj), 'ANC')

    def test_clinic_type_smc(self):
        for referral_code in ['SMC-UNK', 'SMC-NEG']:
            with self.subTest(referral_code=referral_code):
                obj = ClinicType(referral_code=referral_code)
                self.assertEqual(str(obj), 'SMC')
