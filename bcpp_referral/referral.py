from django.core.exceptions import ObjectDoesNotExist

from edc_constants.constants import POS, NEG, MALE, FEMALE, NAIVE, YES, UNK
# from edc_map.site_mappers import site_mappers
from edc_metadata.models import CrfMetadata
from edc_metadata.constants import REQUIRED, KEYED


# from ..models import ReproductiveHealth, is_circumcised, HivCareAdherence
# from ..subject_helper import SubjectHelper, ON_ART, DEFAULTER
from .choices import REFERRAL_CODES
from .constants import URGENT_REFERRALS
from .referral_appt import ReferralAppt
from .referral_code import ReferralCode


class ReferralError(Exception):
    pass


class DataHelper:

    def __init__(self, subject_visit=None, gender=None, **kwargs):
        self.gender = gender
        self.subject_visit = subject_visit
        self.subject_identifier = subject_visit.subject_identifier
        try:
            pima_cd4 = self.subject_visit.pimacd4
        except ObjectDoesNotExist:
            self.cd4_result = None
            self.cd4_result_datetime = None
        else:
            self.cd4_result = pima_cd4.result_value
            self.cd4_result_datetime = pima_cd4.result_datetime
        try:
            hiv_care_adherence = self.subject_visit.hivcareadherence
        except ObjectDoesNotExist:
            try:
                subject_referral = subject_visit.subjectreferral
            except ObjectDoesNotExist:
                self.scheduled_appt_date = None
            else:
                self.scheduled_appt_date = subject_referral.scheduled_appt_date
        else:
            self.scheduled_appt_date = hiv_care_adherence.next_appointment_date


class MaleDataHelper(DataHelper):
    def __init__(self, circumcised=None, **kwargs):
        super().__init__(**kwargs)
        self.circumcised = circumcised


class FemaleDataHelper(DataHelper):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            reproductive_health = self.subject_visit.reproductivehealth
        except ObjectDoesNotExist:
            self.pregnant = None
        else:
            self.pregnant = (
                True if reproductive_health.currently_pregnant == YES else False)


class Referral:
    """A class that calculates the referral code or returns
    a blank string.
    """

    referral_appt_cls = ReferralAppt
    referral_code_cls = ReferralCode

    def __init__(self, subject_status_cls=None, data_helper_cls=None, **kwargs):
        self.data_helper = data_helper_cls(**kwargs)
        self.subject_visit = self.data_helper.subject_visit
        self.subject_status = subject_status_cls(self.subject_visit)
        self.subject_identifier = self.data_helper.subject_identifier

        self.referral_code = self.referral_code_cls(**kwargs).referral_code
        # from referral appt
        self.referral_appt = self.referral_appt_cls(
            self.referral_code,
            base_date=self.subject_visit.report_datetime,
            scheduled_appt_date=self.helper.scheduled_appt_date)

        # from mapper
        self.intervention = site_mappers.get_mapper(
            site_mappers.current_map_area).intervention
        self.community_code = site_mappers.get_mapper(
            site_mappers.current_map_area).map_code

        self.urgent_referral = self.referral_code in URGENT_REFERRALS

#     def __repr__(self):
#         return f'{self.__class__.__name__}()'

    def __str__(self):
        return f'{self.subject_identifier}: {self.referral_code}'


#     def previous_subject_referrals(self):
#         internal_identifier = (
#             self.subject_referral.subject_visit.household_member.internal_identifier)
#         return (
#             self.subject_referral.__class__.objects.filter(
#                 subject_visit__household_member__internal_identifier=internal_identifier,
#                 report_datetime__lt=self.subject_referral.report_datetime).order_by(
#                     'report_datetime'))

    @property
    def cd4_required(self):
        try:
            return CrfMetadata.objects.get(
                model='bcpp_subject.pimacd4',
                entry_status__in=[REQUIRED, KEYED],
                visit_code=self.subject_visit.visit_code,
                subject_identifier=self.subject_visit.subject_identifier)
        except CrfMetadata.DoesNotExist:
            return None
