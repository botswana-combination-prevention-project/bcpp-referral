from datetime import datetime
from django.test import TestCase, tag

from edc_constants.constants import MALE, YES
from edc_registration.models import RegisteredSubject

from bcpp_status import StatusHelper

from ..data_helpers import DataHelper, ReferralDataError, MaleDataHelper, FemaleDataHelper
from ..referral import Referral
from .models import SubjectVisit, SubjectReferral, ReproductiveHealth, HivCareAdherence, PimaCd4


class TestReferral(TestCase):

    def test_referral(self):
        subject_identifier = '111111'
        subject_visit = SubjectVisit(subject_identifier=subject_identifier)
        gender = MALE
        Referral(
            gender=gender,
            subject_visit=subject_visit,
            status_helper_cls=StatusHelper)
