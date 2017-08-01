
from dateutil.relativedelta import TU, WE
from django.test import TestCase, tag
from django.test.client import RequestFactory
from django.views.generic.base import ContextMixin
from edc_appointment.facility import Facility

from edc_constants.constants import POS, NAIVE, MALE
from edc_registration.models import RegisteredSubject

from ..referral import Referral
from ..referral_facility import ReferralFacility, ReferralFacilities
from ..referral_view_mixin import ReferralViewMixin
from .models import SubjectVisit
from .reference_config_helper import ReferenceConfigHelper


class MyView(ReferralViewMixin, ContextMixin):

    pass


class TestView(TestCase):

    reference_config_helper = ReferenceConfigHelper()

    def setUp(self):
        # reconfig reference configs to use app_label = bcpp_referral
        self.reference_config_helper.reconfigure('bcpp_referral')

        self.subject_identifier = '12345'
        self.view = MyView()
        request = RequestFactory()

        self.view.request = request
        self.view.request.META = {'HTTP_CLIENT_IP': '1.1.1.1'}
        self.view.request.GET = request
        self.view.object_list = None
        self.view.kwargs = {}

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

    def test_none(self):
        self.view.subject_visit = None
        context = self.view.get_context_data()
        self.assertIsNone(context.get('referral'))

    def test_with_subject(self):

        class StatusHelper:

            visit_model = 'bcpp_referral.subjectvisit'

            def __init__(self, visit=None, **kwargs):
                self.final_hiv_status = POS
                self.final_arv_status = NAIVE
                self.newly_diagnosed = True
                self.declined = False

        class MyReferral(Referral):
            status_helper_cls = StatusHelper

        self.view.referral_cls = MyReferral

        subject_identifier = '111111'
        RegisteredSubject.objects.create(
            subject_identifier=subject_identifier,
            gender=MALE)
        subject_visit = SubjectVisit.objects.create(
            subject_identifier=subject_identifier)

        self.view.subject_visit = subject_visit
        context = self.view.get_context_data()
        self.assertIsNotNone(context.get('referral'))
