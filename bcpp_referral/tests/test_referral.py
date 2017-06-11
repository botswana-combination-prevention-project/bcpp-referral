from django.test import TestCase, tag
from dateutil.relativedelta import TU, WE

from edc_appointment.facility import Facility
from edc_constants.constants import MALE

from bcpp_status import StatusHelper

from ..data_helpers import MaleDataHelper
from ..referral import Referral
from ..referral_facility import ReferralFacility, ReferralFacilities
from .models import SubjectVisit, SubjectReferral, ReproductiveHealth, HivCareAdherence, PimaCd4
from edc_registration.models import RegisteredSubject


class TestReferral(TestCase):

    def setUp(self):
        self.facility1 = Facility(
            name='nijmegen', days=[TU, WE], forward_only=True)
        self.facility2 = Facility(
            name='leiden', days=[TU, WE], forward_only=True)
        referral_facility1 = ReferralFacility(
            facility=self.facility1, routine_codes=['A'], urgent_codes=['B'])
        referral_facility2 = ReferralFacility(
            facility=self.facility2, routine_codes=['C'], urgent_codes=['D'])
        self.facilities = ReferralFacilities(name='test')
        self.facilities.add_facility(facility=referral_facility1)
        self.facilities.add_facility(facility=referral_facility2)

    @tag('1')
    def test_referral(self):
        subject_identifier = '111111'
        RegisteredSubject.objects.create(
            subject_identifier=subject_identifier,
            gender=MALE)
        subject_visit = SubjectVisit(subject_identifier=subject_identifier)
        Referral(
            data_helper_cls=MaleDataHelper,
            referral_facilities=self.facilities,
            gender=MALE,
            subject_visit=subject_visit,
            status_helper_cls=StatusHelper)
