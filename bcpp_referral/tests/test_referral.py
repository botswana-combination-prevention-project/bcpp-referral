from django.test import TestCase, tag
from dateutil.relativedelta import TU, WE

from edc_appointment.facility import Facility
from edc_constants.constants import MALE, POS, NAIVE
from edc_registration.models import RegisteredSubject

from ..referral import Referral
from ..referral_facility import ReferralFacility, ReferralFacilities
from .models import SubjectVisit
from .reference_config_helper import ReferenceConfigHelper


class TestReferral(TestCase):

    reference_config_helper = ReferenceConfigHelper()

    def setUp(self):
        self.reference_config_helper.reconfigure('bcpp_referral')

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

        class StatusHelper:
            def __init__(self, **kwargs):
                self.final_hiv_status = POS
                self.final_arv_status = NAIVE
                self.newly_diagnosed = True
                self.declined = False

        subject_identifier = '111111'
        RegisteredSubject.objects.create(
            subject_identifier=subject_identifier,
            gender=MALE)
        subject_visit = SubjectVisit.objects.create(
            subject_identifier=subject_identifier)
        Referral(
            subject_visit=subject_visit,
            referral_facilities=self.facilities,
            status_helper_cls=StatusHelper)

    def test_referral_facility(self):
        class StatusHelper:
            def __init__(self, **kwargs):
                self.final_hiv_status = POS
                self.final_arv_status = NAIVE
                self.newly_diagnosed = True
                self.declined = False

        subject_identifier = '111111'
        RegisteredSubject.objects.create(
            subject_identifier=subject_identifier,
            gender=MALE)
        subject_visit = SubjectVisit.objects.create(
            subject_identifier=subject_identifier)
        referral = Referral(
            subject_visit=subject_visit,
            referral_facilities=self.facilities,
            status_helper_cls=StatusHelper)
        self.assertEqual(referral.facility.name, 'nijmegen')

    def test_referral_facility_referral_appt_datetime(self):
        class StatusHelper:
            def __init__(self, **kwargs):
                self.final_hiv_status = POS
                self.final_arv_status = NAIVE
                self.newly_diagnosed = True
                self.declined = False
        subject_identifier = '111111'
        RegisteredSubject.objects.create(
            subject_identifier=subject_identifier,
            gender=MALE)
        subject_visit = SubjectVisit.objects.create(
            subject_identifier=subject_identifier)
        referral = Referral(
            subject_visit=subject_visit,
            referral_facilities=self.facilities,
            status_helper_cls=StatusHelper)
        self.assertIsNotNone(referral.referral_appt_datetime)

    def test_referral_facility_urgent_referral(self):
        class StatusHelper:
            def __init__(self, **kwargs):
                self.final_hiv_status = POS
                self.final_arv_status = NAIVE
                self.newly_diagnosed = True
                self.declined = False
        subject_identifier = '111111'
        RegisteredSubject.objects.create(
            subject_identifier=subject_identifier,
            gender=MALE)
        subject_visit = SubjectVisit.objects.create(
            subject_identifier=subject_identifier)
        referral = Referral(
            subject_visit=subject_visit,
            referral_facilities=self.facilities,
            status_helper_cls=StatusHelper)
        self.assertTrue(referral.urgent_referral)
