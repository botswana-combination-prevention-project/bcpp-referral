from datetime import datetime
from django.test import TestCase, tag

from edc_constants.constants import MALE, YES, FEMALE, NO
from edc_registration.models import RegisteredSubject

from ..data_getter import DataGetter, ReferralDataGetterError
from .models import SubjectVisit, SubjectReferral, ReproductiveHealth
from .models import HivCareAdherence, PimaCd4, Circumcision
from .reference_config_helper import ReferenceConfigHelper


class TestDataHelper(TestCase):

    reference_config_helper = ReferenceConfigHelper()

    def setUp(self):
        self.reference_config_helper.reconfigure('bcpp_referral')
        self.subject_identifier_male = '1111111'
        self.subject_identifier_female = '2222222'
        self.subject_visit = SubjectVisit.objects.create(
            subject_identifier=self.subject_identifier_male)
        self.subject_visit_male = self.subject_visit
        self.subject_visit_female = SubjectVisit.objects.create(
            subject_identifier=self.subject_identifier_female)
        RegisteredSubject.objects.create(
            subject_identifier=self.subject_identifier_male, gender=MALE)
        RegisteredSubject.objects.create(
            subject_identifier=self.subject_identifier_female, gender=FEMALE)

    def test_not_registered_raises(self):
        """Assert works if no data other than subject visit.
        """
        RegisteredSubject.objects.all().delete()
        self.assertRaises(
            ReferralDataGetterError, DataGetter, subject_visit=self.subject_visit)

    def test_data_helper_nulls(self):
        """Assert works if no data other than subject visit.
        """
        data_helper = DataGetter(subject_visit=self.subject_visit)
        self.assertEqual(data_helper.subject_visit, self.subject_visit)
        self.assertEqual(
            data_helper.subject_identifier, self.subject_identifier_male)
        self.assertEqual(data_helper.cd4_result, None)
        self.assertEqual(data_helper.cd4_result_datetime, None)
        self.assertEqual(data_helper.scheduled_appt_date, None)

    def test_data_helper_iter(self):
        """Assert can iterate over instance.
        """
        data_helper = DataGetter(subject_visit=self.subject_visit)
        for index, _ in enumerate(data_helper):
            pass
        self.assertGreater(index, 0)

    @tag('2')
    def test_data_helper_with_models(self):
        PimaCd4.objects.create(subject_visit=self.subject_visit,
                               result_value=None, result_datetime=None)
        HivCareAdherence.objects.create(subject_visit=self.subject_visit)
        SubjectReferral.objects.create(subject_visit=self.subject_visit)
        data_getter = DataGetter(subject_visit=self.subject_visit)
        self.assertEqual(data_getter.subject_visit, self.subject_visit)
        self.assertEqual(
            data_getter.subject_identifier, self.subject_identifier_male)
        self.assertEqual(data_getter.cd4_result, None)
        self.assertEqual(data_getter.cd4_result_datetime, None)
        self.assertEqual(data_getter.scheduled_appt_date, None)
        self.assertEqual(data_getter.gender, MALE)

    def test_data_helper_appt_date_from_referral(self):
        """Assert chooses referral date if no other date.
        """
        referral_dt = datetime(2001, 12, 1)
        PimaCd4.objects.create(
            subject_visit=self.subject_visit,
            result_value=None,
            result_datetime=None)
        HivCareAdherence.objects.create(
            subject_visit=self.subject_visit,
            next_appointment_date=None)
        SubjectReferral.objects.create(
            subject_visit=self.subject_visit,
            scheduled_appt_date=referral_dt)
        data_getter = DataGetter(subject_visit=self.subject_visit)
        self.assertEqual(data_getter.scheduled_appt_date, referral_dt)

    def test_data_helper_appt_date_from_hivcareadherence(self):
        """Assert chooses hivcareadherence date over referral date.
        """
        appt_date1 = datetime(2001, 12, 1)
        PimaCd4.objects.create(subject_visit=self.subject_visit,
                               result_value=None, result_datetime=None)
        HivCareAdherence.objects.create(subject_visit=self.subject_visit,
                                        next_appointment_date=appt_date1)
        for referral_dt in [None, datetime(2001, 12, 2)]:
            with self.subTest(referral_dt=referral_dt):
                SubjectReferral.objects.create(subject_visit=self.subject_visit,
                                               scheduled_appt_date=referral_dt)
                data_getter = DataGetter(subject_visit=self.subject_visit)
                self.assertEqual(data_getter.scheduled_appt_date, appt_date1)
                SubjectReferral.objects.all().delete()

    def test_male_data_helper_unknown_circumcision(self):
        data_getter = DataGetter(subject_visit=self.subject_visit)
        self.assertIsNone(data_getter.circumcised)

    def test_male_data_helper_circumcision1(self):
        Circumcision.objects.create(
            subject_visit=self.subject_visit,
            circumcised=NO)
        data_getter = DataGetter(subject_visit=self.subject_visit)
        self.assertFalse(data_getter.circumcised)

    def test_male_data_helper_circumcision2(self):
        Circumcision.objects.create(
            subject_visit=self.subject_visit,
            circumcised=YES)
        data_getter = DataGetter(subject_visit=self.subject_visit)
        self.assertTrue(data_getter.circumcised)

    def test_female_data_helper_unknown_pregnant(self):
        data_getter = DataGetter(subject_visit=self.subject_visit_female)
        self.assertIsNone(data_getter.pregnant)

    def test_female_data_helper_not_pregnant(self):
        ReproductiveHealth(subject_visit=self.subject_visit_female,
                           currently_pregnant=NO)
        data_getter = DataGetter(subject_visit=self.subject_visit_female)
        self.assertFalse(data_getter.pregnant)

    def test_female_data_helper_pregnant(self):
        ReproductiveHealth(subject_visit=self.subject_visit_female,
                           currently_pregnant=YES)
        data_getter = DataGetter(subject_visit=self.subject_visit_female)
        self.assertTrue(data_getter.pregnant)
