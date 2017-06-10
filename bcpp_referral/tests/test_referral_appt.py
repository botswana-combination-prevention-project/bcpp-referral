from django.test import TestCase, tag

from edc_appointment.facility import Facility
from edc_constants.constants import MALE, YES, POS

from ..referral_appt import ReferralAppt
from ..referral_code import ReferralCode
from .models import SubjectVisit, SubjectReferral, ReproductiveHealth, HivCareAdherence, PimaCd4


class TestReferralAppt(TestCase):

    @tag('1')
    def test_appt_repr(self):
        referral_appt = ReferralAppt(referral_code='MASA-CC')
        self.assertTrue(repr(referral_appt))

    @tag('1')
    def test_appt(self):
        facility = Facility()
        ReferralAppt(referral_code='MASA-CC', facility=facility)
