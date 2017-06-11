from django.test import TestCase, tag
from dateutil.relativedelta import TU, WE

from edc_appointment.facility import Facility
from edc_constants.constants import MALE, POS, NAIVE
from edc_registration.models import RegisteredSubject

from ..data_helper import DataHelper
from ..referral import Referral
from ..referral_facility import ReferralFacility, ReferralFacilities
from .models import SubjectVisit
from .mocks import MockStatusHelper


class TestReferral(TestCase):

    def setUp(self):
        self.facility1 = Facility(
            name='nijmegen', days=[TU, WE], forward_only=True)
        self.facility2 = Facility(
            name='leiden', days=[TU, WE], forward_only=True)
        referral_facility1 = ReferralFacility(
            facility=self.facility1, routine_codes=['A'], urgent_codes=['POS#NVE', 'POS!NVE'])
        referral_facility2 = ReferralFacility(
            facility=self.facility2, routine_codes=['C'], urgent_codes=['D'])
        self.facilities = ReferralFacilities(name='test')
        self.facilities.add_facility(facility=referral_facility1)
        self.facilities.add_facility(facility=referral_facility2)

    def test_referral(self):
        subject_identifier = '111111'
        RegisteredSubject.objects.create(
            subject_identifier=subject_identifier,
            gender=MALE)
        subject_visit = SubjectVisit.objects.create(
            subject_identifier=subject_identifier)
        data_helper = DataHelper(subject_visit=subject_visit)
        status_helper = MockStatusHelper(
            final_hiv_status=POS, final_arv_status=NAIVE)
        data = {}
        data.update(**data_helper.data)
        data.update(**status_helper.__dict__)
        Referral(referral_facilities=self.facilities, **data)

    def test_referral_facility(self):
        subject_identifier = '111111'
        RegisteredSubject.objects.create(
            subject_identifier=subject_identifier,
            gender=MALE)
        subject_visit = SubjectVisit.objects.create(
            subject_identifier=subject_identifier)
        data_helper = DataHelper(subject_visit=subject_visit)
        status_helper = MockStatusHelper(
            final_hiv_status=POS, final_arv_status=NAIVE)
        data = {}
        data.update(**data_helper.data)
        data.update(**status_helper.__dict__)
        referral = Referral(referral_facilities=self.facilities, **data)
        self.assertEqual(referral.facility.name, 'nijmegen')

    def test_referral_facility_referral_appt_datetime(self):
        subject_identifier = '111111'
        RegisteredSubject.objects.create(
            subject_identifier=subject_identifier,
            gender=MALE)
        subject_visit = SubjectVisit.objects.create(
            subject_identifier=subject_identifier)
        data_helper = DataHelper(subject_visit=subject_visit)
        status_helper = MockStatusHelper(
            final_hiv_status=POS, final_arv_status=NAIVE)
        data = {}
        data.update(**data_helper.data)
        data.update(**status_helper.__dict__)
        referral = Referral(referral_facilities=self.facilities, **data)
        self.assertIsNotNone(referral.referral_appt_datetime)

    def test_referral_facility_urgent_referral(self):
        subject_identifier = '111111'
        RegisteredSubject.objects.create(
            subject_identifier=subject_identifier,
            gender=MALE)
        subject_visit = SubjectVisit.objects.create(
            subject_identifier=subject_identifier)
        data_helper = DataHelper(subject_visit=subject_visit)
        status_helper = MockStatusHelper(
            final_hiv_status=POS, final_arv_status=NAIVE)
        data = {}
        data.update(**data_helper.data)
        data.update(**status_helper.__dict__)
        referral = Referral(referral_facilities=self.facilities, **data)
        self.assertTrue(referral.urgent_referral)
