from datetime import datetime
from django.test import TestCase, tag

from edc_constants.constants import MALE, YES, POS
from edc_registration.models import RegisteredSubject

from ..referral_appt import ReferralAppt
from .models import SubjectVisit, SubjectReferral, ReproductiveHealth, HivCareAdherence, PimaCd4
from bcpp_referral.referral_code.referral_code import ReferralCode
from bcpp_referral.referral_appt import ClinicType


class TestReferralAppt(TestCase):

    @tag('1')
    def test_appt_repr(self):
        referral_appt = ReferralAppt()
        self.assertTrue(repr(referral_appt))

    @tag('1')
    def test_appt(self):
        referral_code = ReferralCode(hiv_status=POS)
        ReferralAppt(referral_code=referral_code)

    @tag('2')
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
