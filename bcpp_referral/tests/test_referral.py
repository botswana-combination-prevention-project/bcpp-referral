from django.db import models
from django.test import TestCase

from edc_constants.constants import MALE
from edc_base.model_mixins.base_uuid_model import BaseUuidModel
from edc_appointment.models import Appointment

from ..referral import DataHelper, Referral


class SubjectVisit(BaseUuidModel):

    appointment = models.ForeignKey(Appointment)

    subject_identifier = models.CharField(max_length=25)


class SubjectHelper:
    def __init__(self, subject_visit=None):
        self.subject_visit = subject_visit


class TestReferral(TestCase):

    def test_data_helper(self):
        data_helper = DataHelper()
        self.assertEqual(data_helper.gender, None)
        self.assertEqual(data_helper.subject_visit, None)
        self.assertEqual(data_helper.subject_identifier, None)
        self.assertEqual(data_helper.cd4_result, None)
        self.assertEqual(data_helper.cd4_result_datetime, None)
        self.assertEqual(data_helper.scheduled_appt_date, None)

    def test_referral(self):
        subject_identifier = '111111'
        subject_visit = SubjectVisit(subject_identifier=subject_identifier)
        gender = MALE
        Referral(
            gender=gender,
            subject_visit=subject_visit,
            subject_helper_cls=SubjectHelper)
