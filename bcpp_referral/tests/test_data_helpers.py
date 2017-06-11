from datetime import datetime
from django.test import TestCase, tag

from edc_constants.constants import MALE, YES
from edc_registration.models import RegisteredSubject

from ..data_helpers import DataHelper, ReferralDataError, MaleDataHelper, FemaleDataHelper
from .models import SubjectVisit, SubjectReferral, ReproductiveHealth, HivCareAdherence, PimaCd4


class TestDataHelper(TestCase):

    def setUp(self):
        self.subject_identifier = '1111111'
        self.subject_visit = SubjectVisit(
            subject_identifier=self.subject_identifier)
        RegisteredSubject.objects.create(
            subject_identifier=self.subject_identifier, gender=MALE)

    def test_not_registered_raises(self):
        """Assert works if no data other than subject visit.
        """
        RegisteredSubject.objects.all().delete()
        self.assertRaises(
            ReferralDataError, DataHelper, subject_visit=self.subject_visit)

    def test_data_helper_nulls(self):
        """Assert works if no data other than subject visit.
        """
        data_helper = DataHelper(subject_visit=self.subject_visit)
        self.assertEqual(data_helper.subject_visit, self.subject_visit)
        self.assertEqual(
            data_helper.subject_identifier, self.subject_identifier)
        self.assertEqual(data_helper.cd4_result, None)
        self.assertEqual(data_helper.cd4_result_datetime, None)
        self.assertEqual(data_helper.scheduled_appt_date, None)

    def test_data_helper_with_models(self):
        PimaCd4(subject_visit=self.subject_visit,
                result_value=None, result_datetime=None)
        HivCareAdherence(subject_visit=self.subject_visit)
        SubjectReferral(subject_visit=self.subject_visit)
        data_helper = DataHelper(subject_visit=self.subject_visit)
        self.assertEqual(data_helper.subject_visit, self.subject_visit)
        self.assertEqual(
            data_helper.subject_identifier, self.subject_identifier)
        self.assertEqual(data_helper.gender, MALE)
        self.assertEqual(data_helper.cd4_result, None)
        self.assertEqual(data_helper.cd4_result_datetime, None)
        self.assertEqual(data_helper.scheduled_appt_date, None)

    def test_data_helper_appt_date_from_referral(self):
        """Assert chooses referral date if no other date.
        """
        referral_dt = datetime(2001, 12, 1)
        PimaCd4(subject_visit=self.subject_visit,
                result_value=None, result_datetime=None)
        HivCareAdherence(subject_visit=self.subject_visit,
                         next_appointment_date=None)
        SubjectReferral(subject_visit=self.subject_visit,
                        scheduled_appt_date=referral_dt)
        data_helper = DataHelper(subject_visit=self.subject_visit)
        self.assertEqual(data_helper.scheduled_appt_date, referral_dt)

    def test_data_helper_appt_date_from_hivcareadherence(self):
        """Assert chooses hivcareadherence date over referral date.
        """
        appt_date1 = datetime(2001, 12, 1)
        PimaCd4(subject_visit=self.subject_visit,
                result_value=None, result_datetime=None)
        HivCareAdherence(subject_visit=self.subject_visit,
                         next_appointment_date=appt_date1)
        for referral_dt in [None, datetime(2001, 12, 2)]:
            with self.subTest(referral_dt=referral_dt):
                SubjectReferral(subject_visit=self.subject_visit,
                                scheduled_appt_date=referral_dt)
                data_helper = DataHelper(subject_visit=self.subject_visit)
                self.assertEqual(data_helper.scheduled_appt_date, appt_date1)

    def test_data_helper_from_kwargs_scheduled_appt_date(self):
        appt_date = datetime(2001, 12, 1)
        options = {'scheduled_appt_date': appt_date}
        data_helper = DataHelper(subject_visit=self.subject_visit, **options)
        self.assertEqual(data_helper.scheduled_appt_date, appt_date)

    def test_data_helper_from_kwargs_cd4_result(self):
        options = {'cd4_result': 100}
        data_helper = DataHelper(subject_visit=self.subject_visit, **options)
        self.assertEqual(data_helper.cd4_result, 100)

    def test_data_helper_from_kwargs_safely_ignores(self):
        """Asserts ignores keywords.
        """
        options = {'blah': 100}
        DataHelper(subject_visit=self.subject_visit, **options)

    def test_male_data_helper(self):
        data_helper = MaleDataHelper(subject_visit=self.subject_visit)
        self.assertIsNone(data_helper.circumcised)

    def test_male_data_helper_circumcised(self):
        data_helper = MaleDataHelper(
            subject_visit=self.subject_visit, circumcised=True)
        self.assertTrue(data_helper.circumcised)

    def test_female_data_helper(self):
        data_helper = FemaleDataHelper(subject_visit=self.subject_visit)
        self.assertIsNone(data_helper.pregnant)

    def test_female_data_helper_pregnant(self):
        data_helper = FemaleDataHelper(
            subject_visit=self.subject_visit, pregnant=True)
        self.assertTrue(data_helper.pregnant)

    def test_female_data_helper_pregnant_from_model(self):
        ReproductiveHealth(subject_visit=self.subject_visit,
                           currently_pregnant=YES)
        data_helper = FemaleDataHelper(
            subject_visit=self.subject_visit, pregnant=True)
        self.assertTrue(data_helper.pregnant)
