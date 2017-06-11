from datetime import datetime
from django.test import TestCase, tag

from edc_constants.constants import MALE, YES, FEMALE, NO
from edc_registration.models import RegisteredSubject

from ..data_helper import DataHelper, ReferralDataError
from .models import SubjectVisit, SubjectReferral, ReproductiveHealth
from .models import HivCareAdherence, PimaCd4, Circumcision
from bcpp_referral.bcpp.data_updater import DataUpdater
from pprint import pprint


@tag('data_helper')
class TestDataHelper(TestCase):

    def setUp(self):
        self.subject_identifier_male = '1111111'
        self.subject_identifier_female = '2222222'
        self.subject_visit = SubjectVisit.objects.create(
            subject_identifier=self.subject_identifier_male)
        self.subject_visit_female = SubjectVisit.objects.create(
            subject_identifier=self.subject_identifier_female)
        RegisteredSubject.objects.create(
            subject_identifier=self.subject_identifier_male, gender=MALE)
        RegisteredSubject.objects.create(
            subject_identifier=self.subject_identifier_female, gender=FEMALE)

    @tag('1')
    def test_not_registered_raises(self):
        """Assert works if no data other than subject visit.
        """
        RegisteredSubject.objects.all().delete()
        self.assertRaises(
            ReferralDataError, DataHelper, subject_visit=self.subject_visit)

    @tag('1')
    def test_data_helper_nulls(self):
        """Assert works if no data other than subject visit.
        """
        data_helper = DataHelper(
            subject_visit=self.subject_visit, data_updater_cls=DataUpdater)
        self.assertEqual(data_helper.data.get(
            'subject_visit'), self.subject_visit)
        self.assertEqual(
            data_helper.data.get('subject_identifier'), self.subject_identifier_male)
        self.assertEqual(data_helper.data.get('cd4_result'), None)
        self.assertEqual(data_helper.data.get('cd4_result_datetime'), None)
        self.assertEqual(data_helper.data.get('scheduled_appt_date'), None)

    @tag('1')
    def test_data_helper_with_models(self):
        PimaCd4.objects.create(subject_visit=self.subject_visit,
                               result_value=None, result_datetime=None)
        HivCareAdherence.objects.create(subject_visit=self.subject_visit)
        SubjectReferral.objects.create(subject_visit=self.subject_visit)
        data_helper = DataHelper(
            subject_visit=self.subject_visit, data_updater_cls=DataUpdater)
        self.assertEqual(data_helper.data.get(
            'subject_visit'), self.subject_visit)
        self.assertEqual(
            data_helper.data.get('subject_identifier'), self.subject_identifier_male)
        self.assertEqual(data_helper.data.get('cd4_result'), None)
        self.assertEqual(data_helper.data.get('cd4_result_datetime'), None)
        self.assertEqual(data_helper.data.get('scheduled_appt_date'), None)
        self.assertEqual(data_helper.data.get('gender'), MALE)

    @tag('1')
    def test_data_helper_appt_date_from_referral(self):
        """Assert chooses referral date if no other date.
        """
        referral_dt = datetime(2001, 12, 1)
        PimaCd4.objects.create(subject_visit=self.subject_visit,
                               result_value=None, result_datetime=None)
        HivCareAdherence.objects.create(subject_visit=self.subject_visit,
                                        next_appointment_date=None)
        SubjectReferral.objects.create(subject_visit=self.subject_visit,
                                       scheduled_appt_date=referral_dt)
        data_helper = DataHelper(
            subject_visit=self.subject_visit, data_updater_cls=DataUpdater)
        self.assertEqual(data_helper.data.get(
            'scheduled_appt_date'), referral_dt)

    @tag('1')
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
                data_helper = DataHelper(
                    subject_visit=self.subject_visit, data_updater_cls=DataUpdater)
                self.assertEqual(data_helper.data.get(
                    'scheduled_appt_date'), appt_date1)
                SubjectReferral.objects.all().delete()

    @tag('1')
    def test_data_helper_from_kwargs_scheduled_appt_date(self):
        appt_date = datetime(2001, 12, 1)
        data = {'scheduled_appt_date': appt_date}
        data_helper = DataHelper(**data)
        self.assertEqual(data_helper.data.get(
            'scheduled_appt_date'), appt_date)

    @tag('1')
    def test_data_helper_from_kwargs_cd4_result(self):
        data = {'cd4_result': 100}
        data_helper = DataHelper(subject_visit=self.subject_visit, **data)
        self.assertEqual(data_helper.data.get('cd4_result'), 100)

    @tag('1')
    def test_data_helper_from_kwargs_safely_ignores(self):
        """Asserts ignores keywords.
        """
        data = {'blah': 100}
        DataHelper(subject_visit=self.subject_visit, **data)

    @tag('1')
    def test_male_data_helper_unknown_circumcision(self):
        data_helper = DataHelper(
            subject_visit=self.subject_visit, data_updater_cls=DataUpdater)
        self.assertIsNone(data_helper.data.get('circumcised'))

    @tag('1')
    def test_male_data_helper_circumcision1(self):
        Circumcision.objects.create(
            subject_visit=self.subject_visit,
            circumcised=NO)
        data_helper = DataHelper(
            subject_visit=self.subject_visit, data_updater_cls=DataUpdater)
        Circumcision.objects.all().delete()
        self.assertFalse(data_helper.data.get('circumcised'))

    @tag('1')
    def test_male_data_helper_circumcision2(self):
        Circumcision.objects.create(
            subject_visit=self.subject_visit,
            circumcised=YES)
        data_helper = DataHelper(
            subject_visit=self.subject_visit, data_updater_cls=DataUpdater)
        Circumcision.objects.all().delete()
        self.assertTrue(data_helper.data.get('circumcised'))

    @tag('1')
    def test_male_data_helper_circumcision_from_kwargs(self):
        data_helper = DataHelper(
            subject_visit=self.subject_visit, circumcised=True)
        self.assertTrue(data_helper.data.get('circumcised'))

    @tag('1')
    def test_female_data_helper(self):
        data_helper = DataHelper(subject_visit=self.subject_visit_female)
        self.assertIsNone(data_helper.data.get('pregnant'))

    @tag('1')
    def test_female_data_helper_pregnant(self):
        data_helper = DataHelper(
            subject_visit=self.subject_visit_female, pregnant=True)
        self.assertTrue(data_helper.data.get('pregnant'))

    @tag('1')
    def test_female_data_helper_pregnant_with_model_favors_kwargs(self):
        ReproductiveHealth(subject_visit=self.subject_visit_female,
                           currently_pregnant=YES)
        data_helper = DataHelper(
            subject_visit=self.subject_visit_female,
            pregnant=False,
            data_updater_cls=DataUpdater)
        self.assertFalse(data_helper.data.get('pregnant'))

    @tag('1')
    def test_female_data_helper_pregnant_model(self):
        ReproductiveHealth(subject_visit=self.subject_visit_female,
                           currently_pregnant=YES)
        data_helper = DataHelper(
            subject_visit=self.subject_visit_female,
            data_updater_cls=DataUpdater)
        self.assertTrue(data_helper.data.get('pregnant'))
