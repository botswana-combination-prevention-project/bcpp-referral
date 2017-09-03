from bcpp_status.status_db_helper import StatusDbHelper

from .data_getter import DataGetter
from .data_getter import ReferralDataGetterError
from .referral_code import ReferralCode
from .referral_code import ReferralCodeError
from .referral_facility import ReferralFacilityNotFound, ReferralFacilityDateError


class Referral:

    referral_code_cls = ReferralCode
    data_getter_cls = DataGetter
    status_helper_cls = StatusDbHelper

    def __init__(self, subject_visit=None, referral_facilities=None,
                 status_helper_cls=None):
        self.facility = None
        self.referral_appt_datetime = None
        self.urgent_referral = None
        self.scheduled_appt_datetime = None
        self.subject_visit = subject_visit
        if status_helper_cls:
            self.status_helper_cls = status_helper_cls
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

        self.scheduled_appt_datetime = data_getter.scheduled_appt_datetime

        try:
            self.facility = referral_facilities.get_facility(
                referral_code=self.referral_code)
        except ReferralFacilityNotFound:
            pass
        else:
            try:
                self.referral_appt_datetime = self.facility.available_datetime(
                    referral_code=self.referral_code,
                    report_datetime=data_getter.report_datetime,
                    scheduled_appt_datetime=self.scheduled_appt_datetime)
            except ReferralFacilityDateError:
                pass
            self.urgent_referral = self.facility.is_urgent(
                referral_code=self.referral_code)

    def __repr__(self):
        return f'{self.__class__.__name__}'

    def __str__(self):
        return f'{self.subject_identifier}: {self.referral_code}'
