from edc_metadata.models import CrfMetadata
from edc_metadata.constants import REQUIRED, KEYED

from .constants import URGENT_REFERRALS
from .referral_appt import ReferralAppt
from .referral_code import ReferralCode


class ReferralError(Exception):
    pass


class Referral:
    """A class that calculates the referral code or returns
    a blank string.
    """

    referral_appt_cls = ReferralAppt
    referral_code_cls = ReferralCode

    def __init__(self, status_helper_cls=None, data_helper_cls=None, **kwargs):
        self.data_helper = data_helper_cls(**kwargs)
        self.subject_visit = self.data_helper.subject_visit
        self.subject_status = status_helper_cls(
            subject_visit=self.subject_visit)
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
