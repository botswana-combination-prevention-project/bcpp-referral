from bcpp_status import StatusHelper

from .referral_code import ReferralCode
from .data_getter import DataGetter
from arrow.arrow import Arrow
from datetime import datetime

from .data_getter import ReferralDataGetterError
from .referral_code import ReferralCodeError
from .referral_facility import ReferralFacilityNotFound


class Referral:

    referral_code_cls = ReferralCode
    data_getter_cls = DataGetter
    status_helper_cls = StatusHelper

    def __init__(self, subject_visit=None, referral_facilities=None,
                 status_helper_cls=None):

        if status_helper_cls:
            self.status_helper_cls = status_helper_cls
        self.subject_visit = subject_visit
        self.subject_identifier = subject_visit.subject_identifier

        data_getter = self.data_getter_cls(subject_visit=subject_visit)
        status_helper = self.status_helper_cls(visit=subject_visit)

        try:
            pregnant = data_getter.pregnant
        except ReferralDataGetterError:
            pregnant = None

        try:
            circumcised = data_getter.circumcised
        except ReferralDataGetterError:
            circumcised = None

        try:
            referral_code_obj = self.referral_code_cls(
                gender=data_getter.gender,
                circumcised=circumcised,
                pregnant=pregnant,
                cd4_result=data_getter.cd4_result,
                final_hiv_status=status_helper.final_hiv_status,
                final_arv_status=status_helper.final_arv_status,
                newly_diagnosed=status_helper.newly_diagnosed,
                declined=status_helper.declined,
            )
        except ReferralCodeError:
            self.referral_code = None
        else:
            self.referral_code = referral_code_obj.referral_code

        if data_getter.scheduled_appt_date:
            dt = data_getter.scheduled_appt_date
            self.scheduled_appt_datetime = Arrow.fromdatetime(
                datetime(dt.year, dt.month, dt.day, 7, 30)).datetime
        else:
            self.scheduled_appt_datetime = None

        try:
            self.facility = referral_facilities.get_facility(
                referral_code=self.referral_code)
        except ReferralFacilityNotFound:
            self.referral_appt_datetime = None
            self.urgent_referral = None
        else:
            self.referral_appt_datetime = self.facility.available_datetime(
                referral_code=self.referral_code,
                report_datetime=data_getter.report_datetime,
                scheduled_appt_datetime=self.scheduled_appt_datetime)
            self.urgent_referral = self.facility.is_urgent(
                referral_code=self.referral_code)

    def __repr__(self):
        return f'{self.__class__.__name__}'

    def __str__(self):
        return f'{self.subject_identifier}: {self.referral_code}'
